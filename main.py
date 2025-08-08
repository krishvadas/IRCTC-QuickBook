import argparse
from gui import IRCTCLauncher
from browser_controller.browser_book import book_tickets
from utils.config_loader import load_config

def run_gui():
    print("💖 Launching app, please wait...")
    app = IRCTCLauncher()
    app.mainloop()

def run_headless():
    print("🧠 Running in headless mode...")
    data = load_config()
    book_tickets(data['train_number'], data)

def main():
    parser = argparse.ArgumentParser(description="IRCTC QuickBook Launcher")
    parser.add_argument('--no-gui', action='store_true', help='Run in headless mode without GUI')
    args = parser.parse_args()

    if args.no_gui:
        run_headless()
    else:
        run_gui()

if __name__ == "__main__":
    main()
