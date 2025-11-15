from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import os
import time

load_dotenv()

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
TINDER_URL = "https://tinder.com/sk"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
website = driver.get(TINDER_URL)

wait = WebDriverWait(driver, timeout=5)
try:
    reject_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'lxn9zzn') and normalize-space(text())='Odmietnuť']"
        ))
    )
    reject_btn.click()

except TimeoutException:
    pass

try:
    login_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'lxn9zzn') and normalize-space(text())='Prihlás sa']"
    ))
    )
    login_button.click()
except TimeoutException:
    pass

try:
    facebook_login =  wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'Mend(a)') and normalize-space(text())='Prihlás sa cez Facebook']"
        ))
    )
    facebook_login.click()
except TimeoutException:
    pass

try:
    base_window = driver.window_handles[0]
    fb_login_window = driver.window_handles[1]
    driver.switch_to.window(fb_login_window)

    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "pass")))
    password_input.send_keys(ACCOUNT_PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable((By.NAME, "login"))
    )
    login_button.click()
    continue_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//span[contains(text(), 'Pokračovať ako El')]"
        ))
    )
    driver.switch_to.window(base_window)
    continue_btn.click()
except IndexError:
    pass

for n in range (100):
    time.sleep(2)
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.gamepad-icon.gamepad-icon-invert')))
        like_icon = driver.find_elements(By.CLASS_NAME, 'gamepad-button-wrapper')[4]
        like_icon.click()
    except NoSuchElementException:
        pass
    except ElementClickInterceptedException:
        try:
            close_x = driver.find_element(By.CLASS_NAME,"close")
            close_x.click()
        except ElementClickInterceptedException:
            not_interested = driver.find_element(By.CLASS_NAME,"lxn9zzn")
            if "Nemám záujem" in not_interested.text:
                not_interested.click()
