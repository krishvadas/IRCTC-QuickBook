from browser_controller.browser_login import automate_login, load_irctc_homepage
from browser_controller.browser_search import click_selected_class_stable, fill_train_search_form
from browser_controller.browser_session import start_browser_session
from browser_controller.browser_utils import solve_captcha, is_loading, wait_for_loading


def book_tickets(train_number, data, page=None, retry_count = 4):
    if page is None:
        page = start_browser_session()
    if 'pgui' not in page.url and not is_loading(page):
        load_irctc_homepage(page)
    for attempt in range(retry_count):
        if attempt > 1:
            page = start_browser_session()
        print(f"Attempting to book tickets: Attempt {attempt+1}")
        try:
            page.set_default_timeout(2000)
            automate_login(page, data["username"], data["password"])
            wait_for_loading(page)
            if 'train-search' in page.url:
                fill_train_search_form(page, data['source'], data['destination'], data['date'], data['coach'], data['quota'])
                wait_for_loading(page)
            if "train-list" in page.url:
                if not page.locator(f'text=({train_number})').count()>0:
                    fill_train_search_form(page, data['source'], data['destination'], data['date'], data['coach'], data['quota'])
                    wait_for_loading(page)
                    page.wait_for_selector("app-train-avl-enq", state='attached', timeout=40000)
                if not click_selected_class_stable(train_number, data['coach'], data["date"], data["quota"], page):
                    print("❌ Booking interrupted")
                    continue
                page.set_default_timeout(2000)
                wait_for_loading(page)
                page.wait_for_selector('text="+ Add Passenger"', timeout=60000)
                print("✅ Train selected")
            if "psgninput" in page.url:
                passenger_entry_and_book(page, data)
                wait_for_loading(page)
                page.wait_for_selector("input[formcontrolname='captcha']", timeout=40000)
                print("✅ Added all passengers successfully")
            if "reviewBooking" in page.url:
                while 'reviewBooking' in page.url:
                    try:
                        if page.locator("input[formcontrolname='captcha']").count() > 0:
                            solve_captcha(page)
                            continue_click(page)
                            wait_for_loading(page)
                        if page.locator("text='Invalid Captcha").count() > 0:
                            solve_captcha(page)
                            continue_click(page)
                            wait_for_loading(page)
                    except:
                        break
                wait_for_loading(page)
                page.wait_for_selector("text='Payment Methods'", state='attached', timeout=40000)

                print("✅ Entering payment page")
            if 'payment' in page.url:
                pay_and_book_click(page)
            if 'pgui' in page.url:
                try:
                    enter_upi(page, data["upi_id"])
                except Exception as e:
                    pass
                break

        except Exception as e:
            print(f"❌ Booking failed: {e}")
            continue

def fill_passenger_fields(page, index, passenger):
    passenger_block = page.locator("app-passenger").nth(index)
    passenger_block.locator('[placeholder="Name"]').fill(passenger["name"])
    passenger_block.locator('[placeholder="Age"]').fill(passenger["age"])
    passenger_block.locator('[formcontrolname="passengerGender"]').select_option(passenger["sex"])
    print(f'✅ Added {passenger["name"]}, {passenger["age"]}/{passenger["sex"]} successfully')

def passenger_entry_and_book(page, data):
    # Replace with the actual URL
    for i, passenger in enumerate(data["saved_passengers"]):
        if i > 0:
            page.click('text="+ Add Passenger"')
            # pass
        fill_passenger_fields(page, i, passenger)
    page.click('text="Consider for Auto Upgradation."')
    try:
        upi_label = page.locator("label", has_text="Pay through BHIM/UPI")
        upi_label.locator("div[role='radio']").click()
        print("✅ UPI payment option selected")
    except:
        pass
    print("✅ Passengers entered")
    continue_click(page)


def continue_click(page):
    continue_button = page.locator("text=Continue")
    try:
        continue_button.nth(0).click()
    except:
        continue_button.nth(1).click()
    print("✅ Click Continue")

def pay_and_book_click(page):
    pay = page.get_by_role("button", name="Pay & Book")
    pay.wait_for(state="visible", timeout=5000)
    try:
        pay.nth(0).click()
    except:
        continue_click(page)
        page.get_by_role("button", name="Pay & Book").click()
    page.wait_for_selector('[name="VPA"]', state='attached', timeout=40000)
    # enter_upi(page, upi_id)


def enter_upi(page, upi_id):
    try:
        qr_button = page.locator('text="Click here to pay through QR"')
        try:
            qr_button.nth(0).click()
        except:
            qr_button.nth(1).click()
    except:
        page.click('#mandateUPI')
        page.wait_for_selector('[name="VPA"]', state='attached')
        upi = page.locator('[name="VPA"]')
        page.set_default_timeout(1000)
        try:
            upi.nth(1).fill(upi_id)
        except:
            upi.nth(0).fill(upi_id)
        page.wait_for_selector('#autoDebitBtn', state='visible')
        page.click('#autoDebitBtn')

