import time
import warnings
from .browser_session import start_browser_session
from .browser_utils import solve_captcha, wait_for_loading

warnings.filterwarnings("ignore", message=".*pin_memory.*", category=UserWarning)

MAX_CAPTCHA_ATTEMPTS = 3


def load_irctc_homepage(page):
    if page.url not in ("https://www.irctc.co.in/nget/booking/train-list", "https://www.irctc.co.in/nget/train-search"):
        page.goto("https://www.irctc.co.in/nget/train-search", wait_until="domcontentloaded", timeout=5000)
        print("🌍 IRCTC page loaded")

def trigger_login_modal(page):
    try:
        page.locator("a.search_btn.loginText", has_text="LOGIN").click()
        print("🖥️ Large screen LOGIN clicked")
        return True
    except:
        try:
            ham_menu = page.locator("i.fa.fa-align-justify")
            try:
                ham_menu.first.click()
            except:
                ham_menu.last.click()
            page.click("button.search_btn")
            print("💻 Windowed menu LOGIN clicked")
            return True
        except Exception as e:
            print(f"❌ Failed to open login modal : {e}")
            return False

def fill_credentials(page, username_text, password_text):
    try:
        page.fill("input[formcontrolname='userid']", username_text)
        page.fill("input[formcontrolname='password']", password_text)
        print("🧠 Credentials filled")
        return True
    except:
        print("❌ Login fields error")
        return False

def submit_login_form(page):
    try:
        page.click("button.train_Search_custom_hover", timeout=2000)
        print("🚀 Login button clicked")
        return True
    except:
        print("⚠️ Already Logged in or SIGN IN button click failed")
        return False

def is_login_modal_open(page):
    # Checks if the login modal is still visible
    value = page.locator("app-login.ng-star-inserted").count() > 0
    return value

def login_check(page):
    if page.locator("a[href='/nget/logout']:has-text('Logout')").count() > 0:
        return True
    else:
        return False


def automate_login(page, username_text, password_text):
    if page is None:
        page = start_browser_session()
    if login_check(page):
        print("✅ Already logged in")
        return
    load_irctc_homepage(page)

    print("🔍 Checking for login form...")
    login_form_visible = page.locator("app-login.ng-star-inserted").count() > 0
    login_clicked = login_form_visible or trigger_login_modal(page)

    if not login_clicked:
        print("🚫 Login trigger failed")
        return

    if not fill_credentials(page, username_text, password_text):
        return

    # 🧩 CAPTCHA retry loop based on modal visibility
    for attempt in range(MAX_CAPTCHA_ATTEMPTS):
        print(f"🔐 CAPTCHA attempt {attempt + 1} of {MAX_CAPTCHA_ATTEMPTS}")
        solve_captcha(page)
        submit_login_form(page)
        wait_for_loading(page)
        if not is_login_modal_open(page):
            print("✅ Login successful, modal closed")
            break
        elif attempt == MAX_CAPTCHA_ATTEMPTS - 1:
            page.locator("a.loginCloseBtn").click()
            automate_login(page, username_text, password_text)

