from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
website = driver.get(GYM_URL)

wait = WebDriverWait(driver, timeout=4)

def login():
    global wait
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    wait.until(EC.presence_of_element_located((By.ID, "home-link")))
    email_input = driver.find_element(By.ID, "email-input")
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)
    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)
    submit_button = driver.find_element(By.ID, "submit-button" )
    submit_button.click()
    wait.until(
        EC.any_of(
           EC.presence_of_element_located((By.ID, "schedule-page")),
           EC.presence_of_element_located((By.ID, "error-message")),
        )
    )

    error_message = driver.find_elements(By.ID, value="error-message")
    if len(error_message) > 0:
        return True
    else:
        return False

def retry(func, retries=7, description=None):
    for i in range(retries):
        result_func = func()
        if result_func == False:
            break

retry(login)

#def book_class():
waitlist = 0
booked_classes = 0
already_booked_or_waitlisted = 0
detailed_class_list = []

processed_days = ["tue","thu", "tomorrow-(tue,","tomorrow-(thu,"]

for day in processed_days:
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div[id^='day-group-{day}']")))

        day_group = driver.find_elements(By.CSS_SELECTOR, f"div[id^='day-group-{day}']")

        class_cards = day_group[0].find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

        for card in class_cards:
            if "6:00 PM" in card.text:
                workout_at_6 = card
                workout_type = workout_at_6.find_element(By.CSS_SELECTOR, 'h3[id^=\'class-name-\']').text
                workout_date = driver.find_element(By.CSS_SELECTOR, f"h2[id^='day-title-{day}']").text
                button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

                if  button.text=="Book Class":
                    def book_specific_class():
                        button.click()
                        wait.until(
                            EC.any_of(
                                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button[id^='book-button-']"), "Booked"),
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id^='class-error']")),
                            )
                        )
                        error = card.find_elements(By.CSS_SELECTOR, "div[id^='class-error']")
                        if len(error) > 0:
                            return True
                        else:
                            return False

                    retry(book_specific_class)

                    booked_classes += 1
                    print(f"✓Booked:{workout_type} on {workout_date}")
                    detailed_class_list.append(f"• [New Booking] {workout_type} on {workout_date}")

                elif button.text=="Booked":
                    already_booked_or_waitlisted += 1
                    print(f"✓Already booked:{workout_type} on {workout_date} ")
                    detailed_class_list.append(f"{workout_type} on {workout_date} already booked.")
                elif button.text=="Join Waitlist":
                    button.click()
                    waitlist += 1
                    print(f"✓Waitlisted:{workout_type} on {workout_date}")
                    detailed_class_list.append(f"• [New Waitlist] {workout_type} on {workout_date}")
                elif button.text=="Waitlisted":
                    already_booked_or_waitlisted += 1
                    print(f"✓Already on waitlist:{workout_type} on {workout_date}")
                    detailed_class_list.append(f"{workout_type} on {workout_date} already waitlisted.")
    except TimeoutException:
        print(f"⚠️ Skipping day {day} – not found.")
        continue

total = waitlist + booked_classes + already_booked_or_waitlisted

print("   =====BOOKING SUMMARY====")
print(f"  Classes booked: {booked_classes}")
print(f"  Waitlists joined: {waitlist}")
print(f"  Already booked / waitlisted: {already_booked_or_waitlisted}")
print(f"  Total Tuesday/Thursday 6pm classes processed: {total}")

print("   =====DETAILED CLASS LIST====")
for detailed_class in detailed_class_list:
    print(detailed_class)

booking_link = driver.find_element(By.ID, value="my-bookings-link")
booking_link.click()

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3[id^='booking-class-name-booking']")))

booked_classes = driver.find_elements(By.CSS_SELECTOR, "h3[id^='booking-class-name-booking']")
booked_classes_count = len(booked_classes)

print("====VERIFYING ON MY BOOKINGS PAGE====")
for booked_class in booked_classes:
    name_booked_class = booked_class.text
    print(f"✓ Verified:{name_booked_class}")

print("====VERIFICATION RESULT====")
print(f"Expected: {total} bookings")
print(f"Found: {booked_classes_count} bookings")

missing_bookings = total - booked_classes_count

if total == booked_classes_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {missing_bookings} bookings")












