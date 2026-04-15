import base64
import numpy as np
from PIL import Image, ImageFilter
from io import BytesIO
import logging
import time
import os
from collections import Counter
import sys
import contextlib
import io

import easyocr

# Disable verbose logging
logging.getLogger("easyocr").disabled = True

# Suppress EasyOCR startup prints (stdout + stderr)
f_out, f_err = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(f_out), contextlib.redirect_stderr(f_err):
    reader = easyocr.Reader(['en'], gpu=False)

# Progressive preprocessing pipeline
def preprocess_image(img, level=0):
    img = img.convert("L")  # Grayscale

    if level == 1:
        img = img.resize((160, 60))  # Resize
    elif level == 2:
        img = img.point(lambda x: 0 if x < 128 else 255)  # Binarize
    elif level == 3:
        img = img.filter(ImageFilter.MedianFilter(size=3))  # Denoise

    return img


def clean_text(text):
    corrections = {
        "|": "J",  # OCR often mistakes J as |
        # Add more as needed
    }
    return "".join(corrections.get(c, c) for c in text)


# OCR with majority vote across attempts
def recognize_captcha(src, max_attempts=5):
    try:
        image_bytes = base64.b64decode(src.split(",")[1])
        img = Image.open(BytesIO(image_bytes)).convert("RGB")

        candidates = []

        for attempt in range(max_attempts):
            processed = preprocess_image(img, level=attempt)
            # detail=0 returns just text strings
            result = reader.readtext(np.array(processed), detail=0)

            if result:
                combined_text = "".join(result).strip()
                print(f"🔍 Attempt {attempt + 1}: {combined_text}")
                candidates.append(combined_text)

        if candidates:
            # Majority vote: pick the most frequent candidate
            final_text = Counter(candidates).most_common(1)[0][0]
            return clean_text(final_text.replace(" ", "").strip())

        print("⚠️ OCR failed to produce any text")
    except Exception as e:
        print(f"⚠️ OCR exception: {e}")
    return ""


# Playwright integration
def solve_captcha(page, input_selector="input[formcontrolname='captcha']"):
    page.set_default_timeout(3000)
    try:
        src = page.locator("img.captcha-img").get_attribute("src")
        captcha_text = recognize_captcha(src)
        page.fill(input_selector, captcha_text)
        print("✅ CAPTCHA filled:", captcha_text)
        return captcha_text
    except Exception as e:
        print(f"❌ CAPTCHA solving failed: {e}")
    return None


def is_loading(page):
    try:
        if page.locator('#loaderP').count() > 0:
            return True
        else:
            return False
    except:
        return False


def wait_for_loading(page):
    for second in range(60):
        if not is_loading(page):
            break
        if is_loading(page):
            print("⌛ Page is loading, please wait")
            time.sleep(1)
