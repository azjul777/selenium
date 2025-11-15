from selenium import webdriver
from InternetSpeedTwitterBot import InternetSpeedTwitterBot
import os
import json
from dotenv import load_dotenv

load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
GMAIL = os.getenv("GMAIL")
X_URL= "https://twitter.com/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

driver = webdriver.Chrome(options=chrome_options)
Bot = InternetSpeedTwitterBot(driver,PROMISED_DOWN,PROMISED_UP)
website = driver.get(X_URL)

with open("cookies.json", "r") as f:
    cookies = json.load(f)

for c in cookies:
    try:
        driver.add_cookie(c)
    except Exception:
        cookie = {k: c[k] for k in ("name","value","domain","path") if k in c}
        driver.add_cookie(cookie)

driver.refresh()

download_speed_value, upload_speed_value = Bot.get_internet_speed()

if download_speed_value <= PROMISED_DOWN and upload_speed_value <= PROMISED_UP:
    Bot.tweet_at_provider()
else:
    print("Internet is ok")


