import json
from datetime import datetime
import customtkinter as ctk
from browser_controller.browser_book import book_tickets
from browser_controller.browser_login import automate_login
from utils.config_loader import load_config, save_config
from sections.login import build_login_section
from sections.train_details import build_train_details_section
from sections.passenger_ui import PassengerManager
from sections.train_select import show_train_selector, fetch_train_options

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class IRCTCLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.train_number_entry = None
        self.page = None
        self.selected_train_number = None
        self.selected_train_class = None
        self.title("🚀 IRCTC Tatkal Launcher")
        self.geometry("600x1000+700+0")

        self.config_data = load_config()
        self.cached_trains = []

        self.button_font = ("Segoe UI Emoji", 12, "bold")
        self.label_font = ("Segoe UI Emoji", 14)

        # Main Scroll Area
        scroll_frame = ctk.CTkScrollableFrame(self, orientation="vertical")
        scroll_frame.pack(side="top", fill="both", expand=True)
        self.scroll_frame = scroll_frame

        # Staggered UI Initialization
        self.after(50, self.build_login_ui)
        self.after(100, self.build_train_details_ui)
        self.after(150, self.build_train_number_ui)
        self.after(200, self.build_search_ui)
        self.after(250, self.build_passenger_ui)
        self.after(300, self.build_launch_button)

        print("✅ Application initialized. Ready for input.")


    def build_login_ui(self):
        self.username, self.password, self.upi_id = build_login_section(
            self.scroll_frame, self.config_data, self.page
        )

    def build_train_details_ui(self):
        self.calendar_context = {
            "calendar": None,
            "root": self,
            "click_binding": None,
            "x": self.winfo_rootx(),
            "y": self.winfo_rooty()
        }

        (self.source, self.dest,
         self.date_entry, self.coach_type,
         self.quota_type) = build_train_details_section(
            self.scroll_frame, self.config_data, self.calendar_context
        )

    def build_train_number_ui(self):
        train_number_section = ctk.CTkFrame(self.scroll_frame)
        train_number_section.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(train_number_section, text="🚂 Train number", font=self.label_font).pack(anchor="w")

        self.train_number_entry = ctk.CTkEntry(
            train_number_section,
            placeholder_text="Train Number"
        )
        self.train_number_entry.pack(fill="x", pady=5)

        if self.config_data.get("train_number"):
            self.train_number_entry.insert(0, self.config_data["train_number"])

        def enforce_numeric_limit(event):
            text = self.train_number_entry.get()
            if not text.isdigit():
                self.train_number_entry.delete(0, "end")
            elif len(text) > 5:
                self.train_number_entry.delete(5, "end")

        self.train_number_entry.bind("<KeyRelease>", enforce_numeric_limit)

    def build_search_ui(self):
        self.selected_train_label = ctk.CTkLabel(self.scroll_frame, text="No train selected", font=self.label_font)
        self.selected_train_label.pack(pady=10)

        search_btn = ctk.CTkButton(
            self.scroll_frame,
            text="🔍 Search Trains",
            command=self.perform_train_search,
            font=self.button_font
        )
        search_btn.pack(pady=10)

        self.select_train_btn = ctk.CTkButton(
            self.scroll_frame,
            text="🚆 Select Train",
            state="disabled",
            command=lambda: show_train_selector(
                parent=self,
                display_label=self.selected_train_label,
                train_list=self.cached_trains
            ),
            font=self.button_font
        )
        self.select_train_btn.pack(pady=5)

    def build_passenger_ui(self):
        self.passenger_manager = PassengerManager(
            self.scroll_frame, self.config_data, self.scroll_frame, self
        )

    def build_launch_button(self):
        launch_btn = ctk.CTkButton(
            self.scroll_frame,
            text="Start Booking 🚀",
            command=self.launch_action,
            font=self.button_font
        )
        launch_btn.pack(pady=20)

    def perform_train_search(self):
        src = self.source.get()
        dst = self.dest.get()
        date = self.date_entry.get() or datetime.today().strftime("%d/%m/%Y")
        coach = self.coach_type.get()
        quota = self.quota_type.get()

        date = self.date_corrector(date)
        trains = fetch_train_options(src, dst, date, coach, quota, self.page)
        if not trains:
            self.select_train_btn.configure(state="disabled")
            self.selected_train_label.configure(text="❌ No train data found.")
            print("🚫 No trains fetched.")
            automate_login(self.page, self.username.get(), self.password.get())
            trains = fetch_train_options(src, dst, date, coach, quota, self.page)

        trains = trains[0]
        self.cached_trains = trains
        print("\n🚆 Available Trains:")
        output = "\n".join(
            f"{t['trainNumber']} | {t['trainName']} | {t['departureTime']} → {t['arrivalTime']} ({t['duration']}) | Classes: {', '.join(t['avlClasses'])}"
            for t in trains
        )
        print(output)
        self.select_train_btn.configure(state="normal")
        self.selected_train_label.configure(text="✅ Train data loaded. Ready to select.")

    def date_corrector(self, date):
        if self.date_entry.get():
            target_date = datetime.strptime(self.date_entry.get(), "%d/%m/%Y").date()
            today = datetime.today().date()
            if target_date < today:
                print("⚠️Warning! Journey date cannot be before today. Falling back to today.️")
                date = today.strftime("%d/%m/%Y")
                self.date_entry.delete(0, "end")
                self.date_entry.insert(0, date)
        return date

    def launch_action(self):
        if not self.passenger_manager.validate_all():
            print("⚠ Please correct passenger details before booking.")
            return

        typed_train_number = self.train_number_entry.get()
        if typed_train_number:
            self.start_booking(typed_train_number)
            return

        if self.selected_train_label.cget("text") == "No train selected" or self.selected_train_number is None:
            print("🛑 Train not selected. Opening train selector...")
            self.perform_train_search()
            selector_win = show_train_selector(self, self.selected_train_label, self.cached_trains)
            if selector_win:
                self.wait_window(selector_win)

        train_number = self.selected_train_number
        if train_number:
            print("✅ Selection complete. Starting booking...")
            self.start_booking(train_number)
        else:
            print("🚫 No selection made. Booking aborted.")

    def start_booking(self, train_number):
        data = {
            "username": self.username.get(),
            "password": self.password.get(),
            "upi_id": self.upi_id.get(),
            "source": self.source.get(),
            "date": self.date_corrector(self.date_entry.get() or datetime.today().strftime("%d/%m/%Y")),
            "destination": self.dest.get(),
            "coach": self.coach_type.get(),
            "quota": self.quota_type.get(),
            "train_number": self.train_number_entry.get(),
            "saved_passengers": self.passenger_manager.get_data()
        }
        print("\n🎯 Booking Launcher Input:")
        print(json.dumps(data, indent=4))
        save_config(data)
        book_tickets(train_number, data, self.page)
