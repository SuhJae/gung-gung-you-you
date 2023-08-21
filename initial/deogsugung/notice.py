import time
import concurrent.futures
from post import GhostPost
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


admin_api_key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
ghost_post = GhostPost(admin_api_key)


options = Options()
# options.add_argument("--headless")
# options.add_experimental_option("detach", True)
# disable images from loading at all
options.add_argument("--blink-settings=imagesEnabled=false")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
bordXpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
articleXpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[3]/div/div"


driver.get("https://www.deoksugung.go.kr/board/list?board_id=NOT")


def getarticle(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, articleXpath)))
    text = driver.find_element(By.XPATH, articleXpath).text

    filename = None
    link = None
    size = None

    if len(driver.find_elements(By.XPATH, "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/a")) > 0:
        link = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/a").get_attribute("href")
        filename = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/a").text
        # temporary request to download the file to find the size
        size = driver.execute_script("return fetch(arguments[0], {method: 'HEAD'}).then(response => response.headers.get('content-length'));", link)

    driver.back()
    return text, filename, link, size


numberOfRows = 1
page = 1
while numberOfRows > 0:
    driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=NOT")
    numberOfRows = len(driver.find_elements(By.XPATH, bordXpath + "/tr"))

    for i in range(1, numberOfRows + 1):
        rowPath = bordXpath + "/tr[" + str(i) + "]"

        articleId = driver.find_element(By.XPATH, rowPath + "/td[1]").text
        if not articleId.isnumeric():
            numberOfRows -= 1
            continue

        title = driver.find_element(By.XPATH, rowPath + "/td[2]/a").text
        url = driver.find_element(By.XPATH, rowPath + "/td[2]/a").get_attribute("href")
        date = driver.find_element(By.XPATH, rowPath + "/td[3]").text

        # check if element inside "/td[4]" has img tag
        if len(driver.find_elements(By.XPATH, rowPath + "/td[4]/img")) > 0:
            isAttachmentIncluded = True
        else:
            isAttachmentIncluded = False

        print(f'{articleId} - {date} - {title} - Attachment: {isAttachmentIncluded}')

        content, filename, link, fileSize = getarticle(url)
        response = ghost_post.create_post(button_url=url, content=content, title=title, tags=["덕수궁", "덕수궁 공지"],
                                          slug="DSUN-" + articleId, string_time=date, is_time_now=False,
                                          filename=filename,
                                          file_url=link, file_size=fileSize)
        print(response)
    print("=============================")
    print(f'page: {page} - number of rows: {numberOfRows}')
    print("=============================")
    page += 1

