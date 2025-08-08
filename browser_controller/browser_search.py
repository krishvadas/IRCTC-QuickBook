import time
from datetime import datetime
import datetime as d
from playwright.sync_api import Page

from utils.variables import AC_COACH, CLASS_CODE_MAP


def fill_train_search_form(
    page: Page,
    from_station: str,
    to_station: str,
    travel_date: str,
    journey_class: str,
    journey_quota: str
):
    # Use lean default timeout for snapping responsiveness
    page.set_default_timeout(3000)

    def log(action: str, value: str, success: bool, error: Exception = None):
        prefix = "✅" if success else "❌"
        print(f"{prefix} {action}: {value}" + (f" | Error: {error}" if not success else ""))

    def from_entry(from_station_local):
        try:
            from_input = page.locator("[formcontrolname='origin'] input[role='searchbox']")
            try:
                page.click("span.fa.fa-pencil", timeout=120)
            except Exception as e:
                pass
            try:
                from_input.nth(0).clear()
                from_input.nth(0).fill(from_station_local)
            except:
                from_input.nth(1).clear()
                from_input.nth(1).fill(from_station_local)
            page.keyboard.press("Tab")
            log("From station", from_station_local, True)
        except Exception as e:
            log("From station", from_station_local, False, e)

    def to_station_fun(to_station_local):
        try:
            to_input = page.locator("[formcontrolname='destination'] input[role='searchbox']")
            try:
                to_input.nth(0).clear()
                to_input.nth(0).fill(to_station_local)
            except:
                to_input.nth(1).clear()
                to_input.nth(1).fill(to_station_local)
            page.keyboard.press("Tab")
            log("To station", to_station_local, True)
        except Exception as e:
            log("To station", to_station_local, False, e)

    def journey_date_and_search(travel_date_local, retry_limit = 2):
        for attempt in range(retry_limit):
            print(f"✅ Entering journey date: {travel_date_local}")
            try:
                date_input = page.locator("[formcontrolname='journeyDate'] input[type='text']")
                try:
                    date_input.nth(0).clear()
                    date_input.nth(0).type(travel_date_local)
                    page.wait_for_timeout(300)
                    date_input.nth(0).press("Enter")
                except Exception as e:
                    date_input.nth(1).clear()
                    date_input.nth(1).type(travel_date_local)
                    page.wait_for_timeout(300)
                    date_input.nth(1).press("Enter")
                log("Journey date", travel_date_local, True)
                if 'train-list' in page.url:
                    return
            except Exception as e:
                log("Journey date", travel_date_local, False, e)
                return
        return

    def class_selection(journey_class_local):
        try:
            page.keyboard.press("Escape")
            class_trigger = page.locator("p-dropdown[formcontrolname='journeyClass'] div[role='button']")
            try:
                class_trigger.nth(0).click()
            except:
                class_trigger.nth(1).click()
            option = page.locator(f"li[role='option'][aria-label='{journey_class_local}']")
            try:
                option.nth(0).scroll_into_view_if_needed()
                option.nth(0).click()
            except Exception as e:
                option.nth(1).scroll_into_view_if_needed()
                option.nth(1).click()
            log("Class selected", journey_class_local, True)
        except Exception as e:
            log("Class selection", journey_class_local, False, e)

    def quota_selection(journey_quota_local):
        try:
            quota_trigger = page.locator("p-dropdown[formcontrolname='journeyQuota'] div[role='button']")
            try:
                quota_trigger.nth(0).click()
            except:
                quota_trigger.nth(1).click()
            option = page.locator(f"li[role='option'][aria-label='{journey_quota_local}']")
            try:
                option.nth(0).scroll_into_view_if_needed()
                option.nth(0).click()
            except:
                option.nth(1).scroll_into_view_if_needed()
                option.nth(1).click()
            log("Quota selected", journey_quota_local, True)
        except Exception as e:
            log("Quota selection", journey_quota_local, False, e)



    def search():
        from_entry(from_station)
        to_station_fun(to_station)
        class_selection(journey_class)
        quota_selection(journey_quota)
        journey_date_and_search(travel_date)

    search()


def click_selected_class_stable(train_number, class_code, date, quota, page:Page):
    trains = page.locator("app-train-avl-enq")
    for i in range(trains.count()):
        train_block = trains.nth(i)
        train_block.scroll_into_view_if_needed()
        page.set_default_timeout(600)

        try:
            # Match using full visible text
            header_text = train_block.locator("div.train-heading").inner_text().strip()
            header_match = train_number in header_text
            if not header_match:
                continue

            if header_match:
                print(f"\n✅ Matched Train Block: {header_text}")
                formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%a, %d %b")
                for j in range(2):
                    wait_if_tomorrow(date, quota, class_code)
                    book_button, class_attr = select_class(class_code, formatted_date, page, train_block)
                    if "disable-book" in class_attr:
                        print("🚫 Book Button is disabled")
                    else:
                        book_button.click()
                        page.wait_for_selector("app-passenger", timeout=10000)
                        return True
                return False
            else:
                print("⚠️ Matching class not found inside verified train block.")
                return False

        except Exception as e:
            print(f"⛔ Error while parsing block {i}: {e}")

    print("🚫 Cannot click the selected class.")
    return False


def select_class(class_code, formatted_date, page, train_block):
    try:
        seat_select = train_block.locator(f"text='{class_code}'")
        seat_select.click()
        print("✅ Class selected successfully")
        seat_select = train_block.locator(f"div.pre-avl:has-text('{formatted_date}')")
        seat_select.click()
    # Locate class blocks using visible class name
    except Exception as e:
        seat_select = train_block.locator(f"text='{CLASS_CODE_MAP.get(class_code)}'")
        seat_select.click()
        print("✅ Class selected successfully")
        page.set_default_timeout(10000)
        seat_select = train_block.locator(f"div.pre-avl:has-text('{formatted_date}')")
        seat_select.click()
        print("✅ Travel date selected successfully")
        page.set_default_timeout(2000)
    book_button = train_block.locator("button.btnDefault.train_Search:has-text('Book Now')")
    class_attr = book_button.get_attribute("class")
    return book_button, class_attr


def wait_if_tomorrow(date_str: str, quota, class_code, wait_till_10am: bool = False):
    if quota not in ['TATKAL', 'PREMIUM TATKAL']:
        return
    target_date = datetime.strptime(date_str, "%d/%m/%Y").date()
    now = datetime.now()
    today = now.date()
    tomorrow = today + d.timedelta(days=1)

    if target_date == tomorrow:
        if class_code in AC_COACH:
            wait_till_10am = True
        hour = 10 if wait_till_10am else 11
        target_time = datetime.combine(today, d.time(hour=hour))
        wait_seconds = (target_time - now).total_seconds()
        if wait_seconds > 0:
            print(f'Waiting for {wait_seconds} seconds...')
            time.sleep(wait_seconds)

