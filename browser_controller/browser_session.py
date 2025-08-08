import os
import socket
import subprocess
import time
from threading import Thread

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

# 🚀 Configuration
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = os.getcwd() + "/.chrome/user_profile"
DEBUG_URL = "http://localhost:9222"

# 🔄 Persistent instances
_playwright = None
_browser: Browser = None
_context: BrowserContext = None

def is_chrome_running() -> bool:
    """Check if Chrome is running with remote debugging."""
    try:
        with socket.create_connection(("localhost", 9222), timeout=0.5):
            return True
    except Exception:
        return False


def launch_chrome():
    print("⚡ Launching Chrome (via cmd)...")
    subprocess.Popen([
        "cmd.exe", "/c", "start", "", CHROME_PATH,
        "--remote-debugging-port=9222",
        f"--user-data-dir={USER_DATA_DIR}",
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
        "--start-maximized",
        "--new-window",
        "--enable-features=NetworkService,NetworkServiceInProcess"
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    shell=True)


def wait_for_chrome(timeout_sec=5) -> bool:
    """Wait until Chrome is listening on debug port."""
    start = time.time()
    while time.time() - start < timeout_sec:
        if is_chrome_running():
            return True
        time.sleep(0.2)
    return False

def launch_and_wait():
    Thread(target=launch_chrome).start()
    return wait_for_chrome()

def reconnect_browser(retries=3, delay=0.5):
    """Reconnect to Chrome if needed."""
    global _playwright, _browser

    if _playwright is None:
        _playwright = sync_playwright().start()

    for _ in range(retries):
        try:
            if _browser is None or not _browser.is_connected():
                print("🔌 Connecting to existing Chrome...")
                _browser = _playwright.chromium.connect_over_cdp(DEBUG_URL)
            return
        except Exception as e:
            print("⚠️ CDP connect failed:", e)
            time.sleep(delay)

    raise RuntimeError("❌ Could not connect to Chrome after retries")

def get_or_create_context() -> BrowserContext:
    """Reuse or create a context in the current browser."""
    global _browser, _context
    try:
        if _context and _context in _browser.contexts:
            return _context
        _context = _browser.contexts[0] if _browser.contexts else _browser.new_context()
        return _context
    except Exception as e:
        print("❌ Failed to get context:", e)
        _context = _browser.new_context()
        return _context

def ensure_page_alive(page: Page) -> Page:
    try:
        if page.is_closed() or 'devtools' in page.url:
            return get_valid_page(_context)
        page.title()  # Trigger a harmless call
        return page
    except Exception:
        return get_valid_page(_context)

def get_valid_page(context: BrowserContext) -> Page:
    """Return a healthy, navigable page."""
    for page in context.pages:
        if not page.is_closed() and 'devtools' not in page.url:
            try:
                return page
            except Exception:
                continue
    return context.new_page()

def start_browser_session() -> Page:
    """Return a stable Page object for automation."""
    global _playwright, _browser, _context

    if not is_chrome_running():
        if not launch_and_wait():
            raise RuntimeError("❌ Chrome did not start")

    reconnect_browser()
    if _browser is None or not _browser.is_connected():
        raise RuntimeError("❌ Could not connect to Chrome")

    print("✅ Chrome session active")

    _context = get_or_create_context()
    page = ensure_page_alive(_context)

    return page

def stop_browser_session():
    """Cleanup local references without affecting Chrome."""
    print("🧹 Releasing Playwright handles...")
    global _playwright, _browser, _context
    try:
        if _context:
            _context = None
        if _browser and _browser.is_connected():
            _browser = None
    except Exception as e:
        print("⚠️ Cleanup error:", e)
    finally:
        _playwright = None
