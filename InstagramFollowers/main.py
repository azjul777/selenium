import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException
import time

load_dotenv()

ACCOUNT_NAME = os.environ.get("ACCOUNT_NAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
INSTAGRAM_URL = "https://www.instagram.com/"
SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

def click_if_visible(driver, xpath, timeout=4):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        try:
            el.click()
            return True
        except (ElementClickInterceptedException, WebDriverException):
            try:
                driver.execute_script("arguments[0].click();", el)
                return True
            except Exception:
                return False
    except TimeoutException:
        return False

class InstaFollower:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, username, password):
        self.driver.get(INSTAGRAM_URL)
        time.sleep(1)

        click_if_visible(self.driver, "//button[contains(., 'Decline')]", timeout=2)
        click_if_visible(self.driver, "//button[contains(., 'Decline optional cookies')]", timeout=2)
        click_if_visible(self.driver, "//button[contains(., 'Allow all cookies')]", timeout=2)

        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.clear()
        password_input.send_keys(password)

        try:
            login_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
            try:
                login_button.click()
            except (ElementClickInterceptedException, WebDriverException):
                self.driver.execute_script("arguments[0].click();", login_button)
        except TimeoutException:
            print("Login button not found")
        time.sleep(2)
        try:
            save_info_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Save info']"))
            )
            self.driver.execute_script("arguments[0].click();", save_info_button)
        except Exception as e:
            pass
        try:
            ok_button = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='button' and normalize-space()='OK']")
                )
            )
            self.driver.execute_script("arguments[0].click();", ok_button)
        except:
            pass
        time.sleep(1)

    def find_followers(self, SIMILAR_ACCOUNT):
        similar_account = self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        followers_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]"))
        )
        followers_link.click()
        time.sleep(1)

    def follow_followers(self, SIMILAR_ACCOUNT):
        button = wait.until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog'] button"))
        )
        while True:
            driver.execute_script(
                 'arguments[0].scrollIntoView({block: "center", behavior: "smooth"});',
                 button
             )
            wait.until(EC.element_to_be_clickable(button))
            if button.text == "Follow":
                button.click()
            try:
                button = button.find_element(By.XPATH, "./following::button[1]")
            except NoSuchElementException:
                break

bot = InstaFollower(driver)
bot.login(ACCOUNT_NAME, ACCOUNT_PASSWORD)
bot.find_followers(SIMILAR_ACCOUNT)
bot.follow_followers(SIMILAR_ACCOUNT)
