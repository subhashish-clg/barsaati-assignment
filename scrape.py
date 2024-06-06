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
import requests

import json
import os
import time
import datetime
import logging
import sys


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


load_dotenv()


def get_trends():
    proxies = {}
    trends_json_object = []

    options = Options()

    if "PROXY" in os.environ:
        options.add_experimental_option("detach", True)
        options.headless = True
        options.add_argument('--proxy-server=%s' % os.environ["PROXY"])
        proxies = {
            "http": f"http://{os.environ['PROXY']}",
            "https": f"http://{os.environ['PROXY']}"
        }

    logger.info("Retrieving IP address for host.")
    IP_ADDRESS = requests.get(
        "https://api.ipify.org/?format=json",
        proxies=proxies
    ).json()["ip"]

    try:
        driver = webdriver.Chrome(options=options)

        logger.info("Visiting X.com.")
        driver.get("https://x.com/login")

        logger.info("Logging in.")

        # Enter username
        element = WebDriverWait(driver, int(os.environ["DELAY_WEBDRIVER"])).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )
        element.send_keys(os.environ["X_USER_EMAIL"])

        element = driver.find_element(By.XPATH, '//span[text()="Next"]')
        element.click()

        element = WebDriverWait(driver, int(os.environ["DELAY_WEBDRIVER"])).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )

        if element:
            element.send_keys(os.environ["X_USERNAME"])

            element = driver.find_element(By.XPATH, '//span[text()="Next"]')
            element.click()

        element = WebDriverWait(driver, int(os.environ["DELAY_WEBDRIVER"])).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']"))
        )
        element.send_keys(os.environ["X_PASSWORD"])

        element = driver.find_element(By.XPATH, '//span[text()="Log in"]')
        element.click()

        driver.implicitly_wait(int(os.environ["DELAY_IMPLICIT"]))  # seconds

        logger.info("Extracting trends.")
        trends = WebDriverWait(driver, int(os.environ["DELAY_WEBDRIVER"])).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '[data-testid="trend"]'))
        )

        logger.info("Processing extracted trends.")
        for trend in trends:
            trending_in, hashtag, additional_description = trend.text.split(
                "\n")

            trends_json_object.append({
                "trending_in": trending_in,
                "hashtag": hashtag.replace("#", ""),
                "additional_description": additional_description
            })

        driver.implicitly_wait(int(os.environ["DELAY_IMPLICIT"]))  # seconds
        logger.info("Closing web driver.")
        driver.close()

        return IP_ADDRESS, trends_json_object

    except:
        return None


if __name__ == "__main__":
    file_path = f"./trends/{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json"

    with open(file_path, "+x") as f:
        IP_ADDRESS, trends = get_trends()
        print(IP_ADDRESS)
        print(trends)
        json.dump(trends, f, sort_keys=True, indent=4)
