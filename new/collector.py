from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

with open("config.json") as f:
    config = json.load(f)

MAX_RETRIES = config["config"]["max_retries"]
RETRY_DELAY = config["config"]["retry_delay"]

options = Options()
# options.add_argument("--headless")
# options.add_experimental_option("detach", True)
options.add_argument("--blink-settings=imagesEnabled=false")  # disable images from loading at all
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def check_bord(bord_xpath: str) -> None:
    rows = driver.find_elements(By.XPATH, bord_xpath)

    for i, row in enumerate(rows, 1):
        print(i)
        print(row.get_attribute('innerHTML'))


def collect_website(name: str) -> None:
    local_config = config[name]
    driver.get(local_config["url"])

    check_bord(local_config["xpath"]["bord"])


collect_website("changdeokgung")
input("Press Enter to continue...")
