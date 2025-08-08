# passenger_buttons.py
import customtkinter as ctk
from customtkinter import CTkCheckBox
from sections.passenger_logic import load_saved_passengers, is_duplicate


def create_dropdown(manager, width=300, height=180):
    saved = load_saved_passengers()
    if not saved:
        print("ℹ No saved passengers to show.")
        return None, None

    dropdown_frame = ctk.CTkToplevel(manager.section)
    dropdown_frame.overrideredirect(True)
    dropdown_frame.transient(manager.section.winfo_toplevel())
    dropdown_frame.configure(fg_color="#2b2b2b")

    scrollable = ctk.CTkScrollableFrame(dropdown_frame, width=width, height=height, orientation="vertical")
    scrollable.pack(fill="both", expand=True)

    bind_scroll_events(scrollable)

    for p in saved:
        cb = CTkCheckBox(
            scrollable,
            text=f"{p['name']} | Age: {p['age']} | Gender: {p['sex']}",
            command=lambda d=p: checkbox_selected(manager, d),
            font=("Arial", 12)
        )
        cb.pack(anchor="w", padx=5, pady=2)

    return dropdown_frame, scrollable


def bind_scroll_events(widget):
    try:
        canvas = widget._parent_canvas
    except AttributeError:
        print("⚠ Scroll binding failed: _parent_canvas not found.")
        return

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 30)), "units")
        return "break"

    def on_linux_scroll_up():
        canvas.yview_scroll(-1, "units")
        return "break"

    def on_linux_scroll_down():
        canvas.yview_scroll(1, "units")
        return "break"

    canvas.bind("<MouseWheel>", on_mousewheel)
    canvas.bind("<Button-4>", on_linux_scroll_up)
    canvas.bind("<Button-5>", on_linux_scroll_down)



def unbind_dropdown_scroll():
    # No-op for CTkScrollableFrame, but kept for compatibility
    pass


def toggle_dropdown(manager):
    if manager.dropdown_frame and not manager.dropdown_frame.winfo_exists():
        manager.dropdown_frame = None
        manager.dropdown_canvas = None

    if manager.dropdown_frame:
        try:
            manager.dropdown_frame.destroy()
        except Exception as e:
            print("⚠ Error destroying dropdown:", e)
        unbind_dropdown_scroll()
        manager.dropdown_frame = None
        manager.dropdown_canvas = None
        if manager.click_binding_id:
            manager.section.winfo_toplevel().unbind("<Button-1>", manager.click_binding_id)
            manager.click_binding_id = None
        return

    try:
        root = manager.section.winfo_toplevel()
        app_x = root.winfo_rootx()
        app_y = root.winfo_rooty()
        app_width = root.winfo_width()
        app_height = root.winfo_height()

        btn_x = manager.dropdown_button.winfo_rootx()
        btn_y = manager.dropdown_button.winfo_rooty()
        btn_height = manager.dropdown_button.winfo_height()

        dropdown_width = 300
        dropdown_height = 180

        predicted_bottom = btn_y + btn_height + dropdown_height
        predicted_right = btn_x + dropdown_width

        dropdown_y = btn_y + btn_height if predicted_bottom <= app_y + app_height else btn_y - dropdown_height
        dropdown_x = btn_x if predicted_right <= app_x + app_width else app_x + app_width - dropdown_width

        manager.dropdown_frame, manager.dropdown_canvas = create_dropdown(manager, width=dropdown_width, height=dropdown_height)
        if manager.dropdown_frame:
            manager.dropdown_frame.geometry(f"{dropdown_width}x{dropdown_height}+{dropdown_x}+{dropdown_y}")
            manager.dropdown_frame.lift()
            manager.section.after(100, lambda: bind_outside_click(manager))
    except Exception as e:
        print("❌ Error creating dropdown:", e)
        manager.dropdown_frame = None
        manager.dropdown_canvas = None


def bind_outside_click(manager):
    root = manager.section.winfo_toplevel()
    manager.click_binding_id = root.bind("<Button-1>", lambda e: global_click_listener(manager, e), add="+")


def global_click_listener(manager, event):
    if not manager.dropdown_frame or not manager.dropdown_frame.winfo_exists():
        manager.dropdown_frame = None
        manager.dropdown_canvas = None
        return

    try:
        if event.widget == manager.dropdown_button:
            return

        x1 = manager.dropdown_frame.winfo_rootx()
        y1 = manager.dropdown_frame.winfo_rooty()
        x2 = x1 + manager.dropdown_frame.winfo_width()
        y2 = y1 + manager.dropdown_frame.winfo_height()
        mx, my = event.x_root, event.y_root

        if not (x1 <= mx <= x2 and y1 <= my <= y2):
            if manager.dropdown_frame.winfo_exists():
                manager.dropdown_frame.destroy()

            manager.dropdown_frame = None
            manager.dropdown_canvas = None

            if manager.click_binding_id:
                root = manager.section.winfo_toplevel()
                root.unbind("<Button-1>", manager.click_binding_id)
                manager.click_binding_id = None
    except Exception as e:
        print("⚠ Error handling outside click:", e)
        manager.dropdown_frame = None
        manager.dropdown_canvas = None


def checkbox_selected(manager, passenger):
    manager.update_add_button_state()
    if not is_duplicate(manager.passenger_rows, passenger):
        manager.add_passenger_row(passenger["name"], passenger["age"], passenger["sex"])
