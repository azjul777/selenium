from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SPEED_URL = "https://www.speedtest.net/"
X_URL= "https://twitter.com/"


class InternetSpeedTwitterBot:
    def __init__(self,driver,down,up):
        self.driver = driver
        self.down = down
        self.up = up

    def get_internet_speed(self):
        wait = WebDriverWait(self.driver, timeout=2)
        wait_test = WebDriverWait(self.driver, timeout=40)
        website = self.driver.get(SPEED_URL)
        try:
            reject_all_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
            )
            reject_all_button.click()
        except TimeoutException:
            pass

        go_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="start speed test - connection type multi"]'))
        )
        go_button.click()

        result_block = wait_test.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.result-item-container.eot-info"))
        )

        download_speed = wait_test.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.result-data-large.number.result-data-value.download-speed"))
        )
        download_speed_value = float(download_speed.text)
        print("Rýchlosť sťahovania:", download_speed.text)
        upload_speed = wait_test.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.result-data-large.number.result-data-value.upload-speed"))
        )
        upload_speed_value = float(upload_speed.text)
        print("Upload speed:", upload_speed.text)

        return (download_speed_value, upload_speed_value)


    def tweet_at_provider(self):
        wait = WebDriverWait(self.driver, timeout=2)
        self.driver.get(X_URL)

        post_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="SideNav_NewTweet_Button"]'))
        )
        post_button.click()

        tweet_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]'))
        )
        tweet_box.send_keys("..")

        tweet_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="tweetButton"]'))
        )
        tweet_button.click()

