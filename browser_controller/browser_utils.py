import base64
import time

import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageFilter
from io import BytesIO
import os
import logging

# Disable PaddleOCR's internal logger before it initializes
logging.getLogger("ppocr").disabled = True

# Load models from project directory
base_dir = os.path.abspath("utils/paddleocr_models")
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    use_gpu=False,
    det_model_dir=os.path.join(base_dir, "det"),
    rec_model_dir=os.path.join(base_dir, "rec"),
    cls_model_dir=os.path.join(base_dir, "cls")
)

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
        "|": "J",  # PaddleOCR often mistakes J as |
        # Add more as needed
    }
    return "".join(corrections.get(c, c) for c in text)


# OCR with confidence-based retry
def recognize_captcha(src, max_attempts=5):
    try:
        image_bytes = base64.b64decode(src.split(",")[1])
        img = Image.open(BytesIO(image_bytes)).convert("RGB")

        best_text = ""
        best_conf = 0.0

        for attempt in range(max_attempts):
            processed = preprocess_image(img, level=attempt)
            result = ocr.ocr(np.array(processed), cls=True)

            if result and result[0]:
                text, confidence = result[0][0][1]
                print(f"🔍 Attempt {attempt + 1}: {text} (Confidence: {confidence:.2f})")

                if confidence > best_conf:
                    best_text = text
                    best_conf = confidence

                if confidence >= 0.98:
                    print("🎯 Confidence threshold met — exiting early")
                    break

        if best_text:
            return clean_text(best_text.replace(" ", "").strip())

        print("⚠️ OCR failed to reach 100% confidence")
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

