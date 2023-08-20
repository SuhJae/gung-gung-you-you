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
options.add_argument("--headless")
# options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
bordXpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody"
articleXpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[4]/td"


driver.get("https://www.cdg.go.kr/cms_for_cdg/process/board/list.jsp?nowPage=1&show_no=23&check_no=4&c_relation=48&c_relation2=110")

# find the last page number
lastPageButton = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[23]/td[2]/table/tbody/tr/td[12]/a")
lastPageButton.click()

elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[5]/td[2]/table/tbody/tr/td")
lastPage = int(elements[-1].text)
print(f'last page: {lastPage}')


def getarticle(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, articleXpath)))
    text = driver.find_element(By.XPATH, articleXpath).text

    filename = None
    link = None
    size = None

    if len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[5]/td/table/tbody/tr/td[3]/a")) > 0:
        link = url
        filename = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[5]/td/table/tbody/tr/td[3]/a").text
        # temporary request to download the file to find the size
        size = 0

    driver.back()
    return text, filename, link, size


max_retries = 5
retry_delay = 3


for page in range(1, lastPage + 1):
    driver.get(f"https://www.cdg.go.kr/cms_for_cdg/process/board/list.jsp?nowPage={page}&show_no=23&check_no=4&c_relation=48&c_relation2=110")

    if page != lastPage:
        numberOfRows = 10
    else:
        numberOfRows = len(driver.find_elements(By.XPATH, bordXpath + "/tr"))

    for i in range(2, numberOfRows * 2 + 2, 2):
        "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[2]/td[1]"
        rowPath = bordXpath + "/tr[" + str(i) + "]"

        articleId = driver.find_element(By.XPATH, rowPath + "/td[1]").text

        title = driver.find_element(By.XPATH, rowPath + "/td[2]/a").text

        url = driver.find_element(By.XPATH, rowPath + "/td[2]/a").get_attribute("href")
        date = driver.find_element(By.XPATH, rowPath + "/td[4]").text

        print(f'{articleId} - {date} - {title}')

        content, filename, link, fileSize = getarticle(url)

        response = ghost_post.create_post(button_url=url, content=content, title=title, tags=["창덕궁"],
                                          slug="CDG-" + articleId, string_time=date, is_time_now=False,
                                          filename=filename,
                                          file_url=link, file_size=fileSize)
        print(response)

driver.quit()