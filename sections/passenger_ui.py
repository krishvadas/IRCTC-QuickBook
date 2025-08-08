# passenger_ui.py
import customtkinter as ctk
import tkinter as tk
from sections.passenger_logic import (
    validate_passengers,
    get_passenger_data,
    is_duplicate
)
from sections.passenger_buttons import toggle_dropdown


class PassengerManager:
    def __init__(self, parent, config_data, canvas, gui):
        self.canvas = canvas
        self.dropdown_frame = None
        self.dropdown_canvas = None
        self.click_binding_id = None
        self.passenger_rows = []
        self.gui = gui
        self.travel_class = gui.quota_type.get() or "GENERAL"
        self.button_font = ("Segoe UI Emoji", 12, "bold")
        self.label_font = ("Segoe UI Emoji", 14)

        self.section = ctk.CTkFrame(parent)
        self.section.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(self.section, text="🧑‍🤝‍🧑 Passengers", font=self.label_font).pack(anchor="w")
        self.container = ctk.CTkFrame(self.section)
        self.container.pack()

        btn_row = ctk.CTkFrame(self.section)
        btn_row.pack(pady=5, fill="x")

        self.add_button = ctk.CTkButton(btn_row, text="➕ Add Passenger", command=self.add_passenger_row, font=self.button_font)
        self.add_button.pack(side="left", padx=5)

        self.dropdown_button = ctk.CTkButton(btn_row, text="🧾 Select from Saved", command=lambda: toggle_dropdown(self), font=self.button_font)
        self.dropdown_button.pack(side="left", padx=5)

        for p in config_data.get("passengers", []):
            self.add_passenger_row(p.get("name", ""), p.get("age", ""), p.get("sex", "M"))
        if not self.passenger_rows:
            self.add_passenger_row()

    def add_passenger_row(self, name="", age="", sex="M"):
        max_passengers = 4 if self.travel_class in ("TATKAL", "PREMIUM TATKAL") else 6
        filled_rows = [r for r in self.passenger_rows if r["name"].get().strip() or r["age"].get().strip()]
        if len(filled_rows) >= max_passengers:
            print(f"⚠ Cannot add more than {max_passengers} passengers for {self.travel_class} class.")
            return

        for row in self.passenger_rows:
            if not row["name"].get().strip() and not row["age"].get().strip():
                row["name"].delete(0, tk.END)
                row["age"].delete(0, tk.END)
                row["sex"].set(sex)
                if name: row["name"].insert(0, name)
                if age: row["age"].insert(0, age)
                return

        frame = ctk.CTkFrame(self.container)
        frame.pack(pady=5, fill="x")
        row = {
            "name": ctk.CTkEntry(frame, placeholder_text="Name"),
            "age": ctk.CTkEntry(frame, placeholder_text="Age"),
            "sex": ctk.CTkComboBox(frame, values=["M", "F"], state="readonly"),
            "frame": frame
        }

        row["name"].pack(side="left", padx=5, expand=True)
        row["age"].pack(side="left", padx=5)
        row["sex"].pack(side="left", padx=5)

        if name: row["name"].insert(0, name)
        if age: row["age"].insert(0, age)
        row["sex"].set(sex)

        def handle_key(event, combo=row["sex"]):
            options = combo.cget("values")
            index = options.index(combo.get())
            combo.set(options[(index - 1) % len(options)] if event.keysym in ("Left", "Up") else options[(index + 1) % len(options)])

        for key in ["<Left>", "<Right>", "<Up>", "<Down>"]:
            row["sex"].bind(key, handle_key)

        def click_combo_arrow(combo=row["sex"]):
            combo.event_generate("<Button-1>", x=combo.winfo_width() - 10, y=combo.winfo_height() // 2)

        row["sex"].bind("<Button-1>", click_combo_arrow)
        row["sex"]._entry.bind("<Button-1>", lambda e: row["sex"]._open_dropdown_menu())

        remove_btn = ctk.CTkButton(
            frame, text="❌ Remove", width=60,
            command=lambda: self.remove_passenger_row(row, frame), font=self.button_font
        )
        remove_btn.pack(side="right", padx=5)

        self.passenger_rows.append(row)
        self.update_remove_buttons()
        self.update_add_button_state()

    def remove_passenger_row(self, row, frame):
        if len(self.passenger_rows) > 1:
            frame.destroy()
            self.passenger_rows.remove(row)
            self.update_remove_buttons()
        self.update_add_button_state()

    def update_remove_buttons(self):
        state = "normal" if len(self.passenger_rows) > 1 else "disabled"
        for r in self.passenger_rows:
            r["frame"].winfo_children()[-1].configure(state=state)

    def validate_all(self):
        return validate_passengers(self.passenger_rows)

    def get_data(self):
        return get_passenger_data(self.passenger_rows)

    def checkbox_selected(self, var, passenger):
        self.update_add_button_state()
        if var.get() and not is_duplicate(self.passenger_rows, passenger):
            self.add_passenger_row(passenger["name"], passenger["age"], passenger["sex"])

    def update_add_button_state(self):
        self.travel_class = self.gui.quota_type.get()
        max_passengers = 4 if self.travel_class in ("TATKAL", "PREMIUM TATKAL") else 6
        filled_rows = [r for r in self.passenger_rows if r["name"].get().strip() or r["age"].get().strip()]
        state = "normal" if len(filled_rows) < max_passengers else "disabled"
        self.add_button.configure(state=state)
        self.dropdown_button.configure(state=state)
