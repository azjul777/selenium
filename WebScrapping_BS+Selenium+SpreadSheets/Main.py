from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from property import Property

URL_ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"
URL_ANSWERS = "https://docs.google.com/forms/d/e/1FAIpQLSc7U3_l0w4yosTLmmE-r4zhpHhBgHPCJPLEkCvrhqtiDheonw/viewform?usp=header"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
time.sleep(1)

def submit_property(property):
    website = driver.get(URL_ANSWERS)
    input_field_address = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
        ))
    )
    input_field_address.send_keys(property.address)
    time.sleep(1)

    input_field_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_field_price.send_keys(property.price)

    input_field_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_field_link.send_keys(property.link)

    submit_button = driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='Submit']")
    submit_button.click()
    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH, "//div[contains(text(), 'Vaša odpoveď je zaznamenaná')]"
        ))
    )
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"}

response = requests.get(url=URL_ZILLOW_CLONE, headers=header)
website_data = response.text
soup = BeautifulSoup(website_data,"html.parser")
property_cards = soup.find_all("article", {"data-test": "property-card"})

for card in property_cards:
    price_tag = card.find("span", {"data-test": "property-card-price"})
    price_raw = price_tag.get_text(strip=True)
    price = ""
    for char in price_raw:
        if char in "$0123456789,":
            price = price + char
    address_tag = card.find("address")
    address = (address_tag.text).strip()
    a_tag = soup.find("a")
    link = a_tag['href']
    property =Property(price, address, link)
    submit_property(property)










