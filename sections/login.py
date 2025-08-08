import customtkinter as ctk
from browser_controller.browser_session import start_browser_session
from browser_controller.browser_login import automate_login

def build_login_section(parent, config_data, page):
    section = ctk.CTkFrame(parent)
    section.pack(pady=10, padx=10, fill="x")

    ctk.CTkLabel(section, text="🔐 Login Section", font=("Segoe UI Emoji", 14)).pack(anchor="w")

    # Create entries early so they can be returned
    username = ctk.CTkEntry(section, placeholder_text="IRCTC Username")
    password = ctk.CTkEntry(section, placeholder_text="IRCTC Password", show="*")
    upi_id = ctk.CTkEntry(section, placeholder_text="UPI Id")

    def pack_and_preload():
        username.pack(fill="x", pady=5)
        password.pack(fill="x", pady=5)
        upi_id.pack(fill="x", pady=5)

        if config_data.get("username"):
            username.insert(0, config_data["username"])
        if config_data.get("password"):
            password.insert(0, config_data["password"])
        if config_data.get("upi_id"):
            upi_id.insert(0, config_data["upi_id"])

        ctk.CTkButton(
            section,
            text="Login",
            command=lambda: login_action(page, username, password)
        ).pack(pady=5)

    section.after(50, pack_and_preload)
    return username, password, upi_id

def login_action(page, username, password):
    uname = username.get().strip()
    pwd = password.get().strip()

    print("🔓 Launching login session...")
    if page is None:
        page = start_browser_session()
    if page:
        print("📶 Browser session active, automating login...")
        automate_login(page, uname, pwd)
    else:
        print("🚫 Login setup failed — browser not launched")
