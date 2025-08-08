from datetime import datetime
import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from utils.station_search import load_station_data, filter_stations
import threading


def build_train_details_section(parent, config_data, calendar_context):
    section = ctk.CTkFrame(parent)
    section.pack(pady=10, padx=10, fill="x")
    ctk.CTkLabel(section, text="🚆 Train Details", font=("Segoe UI Emoji", 14)).pack(anchor="w")

    station_pool = []

    def load_stations_async():
        stations = load_station_data()
        station_pool.clear()
        station_pool.extend(stations)
        # Optionally, update UI here if needed

    threading.Thread(target=load_stations_async, daemon=True).start()

    # 🔁 Source & Destination
    fields = {}
    for key in ["source", "destination"]:
        entry = ctk.CTkEntry(section, placeholder_text=f"{key.capitalize()} Station")
        entry.pack(fill="x", pady=5)
        if config_data.get(key): entry.insert(0, config_data[key])
        attach_station_search(entry, section, station_pool)
        fields[key] = entry

    # 📅 Journey Date
    date_row = ctk.CTkFrame(section); date_row.pack(fill="x", pady=5)
    date_entry = ctk.CTkEntry(date_row, placeholder_text="Journey Date (DD/MM/YYYY)")
    date_entry.pack(side="left", fill="x", expand=True)
    date_button = ctk.CTkButton(date_row, text="📅", width=50,
        command=lambda: toggle_calendar(calendar_context, date_entry))
    date_button.pack(side="right")
    date_entry.bind("<Button-1>", lambda e: toggle_calendar(calendar_context, date_entry))
    date_entry.bind("<Double-Button-1>", lambda e: date_entry.configure(state="normal"))
    if config_data.get("date"): date_entry.insert(0, config_data["date"])

    # 🪑 Coach & Quota Dropdowns
    def add_dropdown(values, default, label):
        dropdown = ctk.CTkComboBox(section, values=values, state="readonly")
        dropdown.pack(fill="x", pady=5)
        dropdown.set(config_data.get(label, default))
        dropdown.bind("<Left>", lambda e: cycle_combo(dropdown, -1))
        dropdown.bind("<Right>", lambda e: cycle_combo(dropdown, 1))
        dropdown.bind("<Up>", lambda e: cycle_combo(dropdown, -1))
        dropdown.bind("<Down>", lambda e: cycle_combo(dropdown, 1))
        # noinspection PyProtectedMember
        dropdown._entry.bind("<Button-1>", lambda e: dropdown._open_dropdown_menu())
        return dropdown

    coach_type = add_dropdown(
        ["All Classes", "Anubhuti Class (EA)", "AC First Class (1A)", "Vistadome AC (EV)", "Exec. Chair Car (EC)",
         "AC 2 Tier (2A)", "First Class (FC)", "AC 3 Tier (3A)", "AC 3 Economy (3E)",
         "Vistadome Chair Car (VC)", "AC Chair car (CC)", "Sleeper (SL)", "Vistadome Non AC (VS)", "Second Sitting (2S)"],
        "All Classes", "coach"
    )

    quota_type = add_dropdown(
        ["GENERAL", "LADIES", "LOWER BERTH/SR.CITIZEN", "PERSON WITH DISABILITY",
         "DUTY PASS", "TATKAL", "PREMIUM TATKAL"],
        "TATKAL", "quota"
    )

    return fields["source"], fields["destination"], date_entry, coach_type, quota_type

def cycle_combo(combo, direction):
    values = combo.cget("values")
    index = values.index(combo.get())
    combo.set(values[(index + direction) % len(values)])


def attach_station_search(entry, parent, station_pool):
    box = tk.Listbox(parent, bg="#1e1e1e", fg="white", font=("Arial", 10), activestyle="none",
                     borderwidth=0, highlightthickness=0)
    box.place_forget()

    selected_index = -1
    last_query = ""
    debounce_timer = None
    search_enabled = True

    def update_suggestions():
        nonlocal selected_index, last_query
        query = entry.get().strip().lower()
        if query == last_query:
            return
        last_query = query
        box.delete(0, tk.END)

        if query:
            matches = filter_stations(query, station_pool)[:6]
            for s in matches:
                text = f"{s['en']} - {s['sc']}" + (f" ({s['ec']})" if s.get("ec") else "")
                box.insert(tk.END, text)
            box.configure(width=max((len(text) for text in box.get(0, tk.END)), default=20) + 4)
            x = entry.winfo_rootx() - parent.winfo_rootx()
            y = entry.winfo_rooty() - parent.winfo_rooty() + entry.winfo_height()
            box.place(x=x, y=y); box.lift(); selected_index = -1
        else:
            box.place_forget()

    def debounced_update(event=None):
        nonlocal debounce_timer, search_enabled
        if event and event.char.isalpha():
            search_enabled = True
        if not search_enabled: return
        search_enabled = True
        if debounce_timer: debounce_timer.cancel()
        from threading import Timer
        debounce_timer = Timer(0.15, lambda: entry.after(0, update_suggestions))
        debounce_timer.start()

    def move_selection(event):
        nonlocal selected_index
        if box.size() == 0: return
        selected_index = (selected_index + (1 if event.keysym == "Down" else -1)) % box.size()
        box.select_clear(0, tk.END)
        box.select_set(selected_index)
        box.activate(selected_index)
        box.see(selected_index)

    def finalize_selection(index):
        nonlocal last_query, search_enabled
        selected = box.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, selected)
        last_query = ""
        search_enabled = False
        box.place_forget()

    def select_station(event):
        nonlocal selected_index
        if selected_index == -1 and box.curselection():
            selected_index = box.curselection()[0]
        if 0 <= selected_index < box.size():
            finalize_selection(selected_index)

    def mouse_select(event):
        if box.curselection():
            finalize_selection(box.curselection()[0])

    entry.bind("<KeyRelease>", debounced_update)
    entry.bind("<Down>", move_selection)
    entry.bind("<Up>", move_selection)
    entry.bind("<Return>", select_station)
    box.bind("<ButtonRelease-1>", mouse_select)


def toggle_calendar(ctx, entry):
    if ctx.get("calendar"):
        close_calendar(ctx); return
    btn = entry.master.winfo_children()[1]
    x = btn.winfo_rootx() - ctx["root"].winfo_rootx() - (btn.winfo_width() * 4)
    y = btn.winfo_rooty() - ctx["root"].winfo_rooty() + btn.winfo_height()

    today = datetime.today()
    cal = Calendar(ctx["root"],
                   selectmode="day",
                   date_pattern="dd/mm/yyyy",
                   mindate=today)  # 🛡️ Prevent selection of past dates
    cal.place(x=x, y=y)
    cal.bind("<<CalendarSelected>>", lambda e: set_date(entry, cal, ctx))
    ctx["calendar"] = cal
    ctx["click_binding"] = ctx["root"].bind("<Button-1>", lambda e: close_calendar(ctx), add="+")


def set_date(entry, cal, ctx):
    entry.delete(0, tk.END)
    entry.insert(0, cal.get_date())
    close_calendar(ctx)


def close_calendar(ctx):
    if ctx.get("calendar"):
        ctx["calendar"].destroy(); ctx["calendar"] = None
    if ctx.get("click_binding"):
        ctx["root"].unbind("<Button-1>", ctx["click_binding"]); ctx["click_binding"] = None
