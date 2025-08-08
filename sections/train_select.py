import json
import time
import customtkinter as ctk
import tkinter as tk
from browser_controller.browser_login import login_check
from browser_controller.browser_search import fill_train_search_form
from browser_controller.browser_session import start_browser_session
from utils.variables import CLASS_CODE_MAP, QUOTA_CODE_MAP, CLASS_NAME_MAP


def fetch_train_options(src, dest, date_str, journey_class_full, quota_full, page):
    if page is None:
        page = start_browser_session()

    if page.url not in ("https://www.irctc.co.in/nget/booking/train-list", "https://www.irctc.co.in/nget/train-search"):
        print("🔗 Navigating to IRCTC booking page...")
        page.goto("https://www.irctc.co.in/nget/train-search", wait_until="domcontentloaded", timeout=5000)

    if login_check(page):
        result = tatkal_trains_search(page, src, dest, date_str, journey_class_full, quota_full)
        if result[1]:
            return result[0]
        if not result[1]:
            result = None
        return result

    try:
        dd, mm, yyyy = date_str.strip().split("/")
        formatted_date = f"{yyyy}{mm}{dd}"
    except Exception as e:
        print(f"❌ Invalid date format: {date_str} | Error: {e}")
        return None

    journey_class = CLASS_CODE_MAP.get(journey_class_full, "")
    quota_code = QUOTA_CODE_MAP.get(quota_full, "")
    src_code = src.split(" - ")[1].split(" ")[0]
    dest_code = dest.split(" - ")[1].split(" ")[0]

    payload = { "concessionBooking": False,
                "srcStn": src_code,
                "destStn": dest_code,
                "jrnyClass": journey_class,
                "jrnyDate": formatted_date,
                "quotaCode": quota_code,
                "currentBooking": "false",
                "flexiFlag": False,
                "handicapFlag": False,
                "ticketType": "E",
                "loyaltyRedemptionBooking": False,
                "ftBooking": False }
    fetch_script = f""" async () => {{ 
                        try {{ 
                        const res = await fetch("https://www.irctc.co.in/eticketing/protected/mapps1/altAvlEnq/TC", 
                        {{ 
                        method: "POST", 
                        headers: 
                        {{ 
                        "accept": "application/json, text/plain, */*",
                        "accept-language": "en-US,en;q=0.0", 
                        "bmirak": "webbm", 
                        "bmiyek": "BB3529CEC7FAD9206CFA84DFC0572DE2", 
                        "content-language": "en", 
                        "content-type": "application/json; charset=UTF-8", 
                        "greq": {str(int(time.time() * 1000))}, 
                        "priority": "u=1, i", 
                        "sec-ch-ua": "Not)A;Brand;v=8, Chromium;v=138, Google Chrome;v=138", 
                        "sec-ch-ua-mobile": "?0", 
                        "sec-ch-ua-platform": "Windows", 
                        "sec-fetch-dest": "empty", 
                        "sec-fetch-mode": "cors", 
                        "sec-fetch-site": "same-origin" 
                        }}, 
                        referrer: "https://www.irctc.co.in/nget/booking/train-list", 
                        body: JSON.stringify({json.dumps(payload)}), 
                        mode: "cors", 
                        credentials: "omit" 
                        }});
                         return await res.json(); 
                         }}
                          catch (err)
                           {{ return {{ error: err.message }}; }} }} """
    result = response_parser(fetch_script, page)
    if result[1]:
        return result
    if not result[1]:
        result = None
    return result

def response_parser(fetch_script, page):
    try:
        result = page.evaluate(fetch_script)
        response = json_parser(result)
        return response
    except Exception as e:
        print(f"❌ Browser evaluate error: {e}")
        return {"error": str(e)}, False

def json_parser(result):
    if not isinstance(result, dict):
        print("🚫 Unexpected result format")
        return {"error": "Invalid response format"}, False
    if result.get("errorMessage"):
        print(f"❌ {result['errorMessage']}")
        if "ARP range" in result["errorMessage"]:
            print("⚠ Journey date selected is outside ARP range.")
        return {"errorMessage": result["errorMessage"]}, False
    if result.get("error"):
        print("❌ JS Fetch error:", result["error"])
        return {"error": result["error"]}, False
    return result.get("trainBtwnStnsList", []), True

def show_train_selector(parent, display_label, train_list):
    if not train_list:
        print("🚫 No trains available.")
        return None

    selector_win = ctk.CTkToplevel(parent)
    selector_win.title("Select Train and Class")
    selector_win.geometry("600x500+350+400")
    selector_win.transient(parent)
    selector_win.lift()
    selector_win.focus_force()

    canvas = tk.Canvas(selector_win, bg="#2b2b2b", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(selector_win, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    frame = ctk.CTkFrame(canvas)
    window_id = canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

    def select_train(parent, train, cls_code):
        label_text = f"{train.get('trainNumber', '')} | {train.get('trainName', '')} | {train.get('departureTime', '')} → {train.get('arrivalTime', '')} | Class selected : {cls_code}"
        display_label.configure(text=label_text)
        selector_win.destroy()
        parent.coach_type.set(CLASS_NAME_MAP.get(cls_code))
        parent.selected_train_number = train.get("trainNumber", "")
        parent.train_number_entry.delete(0, "end")
        parent.train_number_entry.insert(0, train.get("trainNumber", ""))
        parent.selected_train_class = cls_code

    for train in train_list:
        box = ctk.CTkFrame(frame)
        box.pack(pady=10, fill="x", padx=10)

        info = f"{train.get('trainNumber', '')} | {train.get('trainName', '')} | {train.get('departureTime', '')} → {train.get('arrivalTime', '')} | Duration: {train.get('duration', '')}"
        ctk.CTkLabel(box, text=info, anchor="w").pack(fill="x", padx=10)

        btn_row = ctk.CTkFrame(box)
        btn_row.pack(pady=5)

        for cls_code in train.get("avlClasses", []):
            btn = ctk.CTkButton(btn_row, text=cls_code, width=60, command=lambda t=train, c=cls_code, p=parent: select_train(p, t, c))
            btn.pack(side="left", padx=4)
    return selector_win

def tatkal_trains_search(page, src, dest, date_str, journey_class_full, quota_full):
    try:
        train_data_buffer = []
        page.set_default_timeout(300000)
        def handle_response(response):
            if "altAvlEnq/TC" in response.url and response.request.resource_type == "xhr":
                try:
                    data = response.json()
                    print(f"\n📡 Response: {response.url}")
                    parsed = json_parser(data)
                    if parsed[1]:
                        train_data_buffer.append(parsed)
                except Exception:
                    print(f"[Handler] ❌ Could not parse JSON from {response.url}")

        page.on("response", handle_response)
        with page.expect_response("**/eticketing/protected/mapps1/**"):
            fill_train_search_form(page, src, dest, date_str, journey_class_full, quota_full)
        page.remove_listener("response", handle_response)
        return train_data_buffer[0], True if train_data_buffer else [], False

    except Exception as e:
        print(f"❌ Error during search: {e}")
        return {"error": str(e)}, False
