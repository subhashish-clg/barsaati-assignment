import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import json
import os
import time
import datetime

load_dotenv()


def get_trends():
    trends_json_object = []

    try:
        driver = webdriver.Chrome()
        driver.get("https://x.com/login")

        # Enter username
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )
        element.send_keys(os.environ["X_USER_EMAIL"])

        element = driver.find_element(By.XPATH, '//span[text()="Next"]')
        element.click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )
        if element:
            element.send_keys(os.environ["X_USERNAME"])

        element = driver.find_element(By.XPATH, '//span[text()="Next"]')
        element.click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']"))
        )
        element.send_keys(os.environ["X_PASSWORD"])

        element = driver.find_element(By.XPATH, '//span[text()="Log in"]')
        element.click()

        trends = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '[data-testid="trend"]'))
        )

        for trend in trends:
            trending_in, hashtag, number_of_posts = trend.text.split("\n")

            trends_json_object.append({
                "trending_in": trending_in,
                "hashtag": hashtag,
                "number_of_post": number_of_posts
            })

    finally:
        driver.close()
        return trends_json_object

# PROXY = "sg.proxymesh.com:31280"

# options = Options()
# options.add_experimental_option("detach", True)
# options.add_argument('--proxy-server=%s' % PROXY)


# driver = webdriver.Chrome(service=Service(
#     ChromeDriverManager().install()), options=options)


if __name__ == "__main__":
    file_path = f"./trends/{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json"

    with open(file_path, "+x") as f:
        trends = get_trends()

        json.dump(trends, f)
