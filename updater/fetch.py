from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from lastpost import LastPostFetcher
from post import GhostPost


class FetchUntil:
    def __init__(self, admin_api_key):
        self.admin_api_key = admin_api_key
        self.ghost_post = GhostPost(admin_api_key)
        self.post_fetcher = LastPostFetcher(admin_api_key)
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def gyeongbokgung_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/form/div/table/tbody"
        article_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[2]/td"
        attachment_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/table/tfoot/tr/td/a"
        page = 1

        while True:
            self.driver.get(f"https://www.royalpalace.go.kr/content/board/list.asp?page={page}")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))
            for i in range(1, number_of_rows + 1):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/th").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return

                    title = self.driver.find_element(By.XPATH, row_path + "/td[1]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[1]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[3]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, size, link = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        link = self.driver.find_element(By.XPATH, attachment_xpath).get_attribute("href")
                        filename = self.driver.find_element(By.XPATH, attachment_xpath).text
                        size = self.driver.execute_script(
                            "return fetch(arguments[0], {method: 'HEAD'}).then(response => response.headers.get('content-length'));",
                            link)
                    self.driver.back()
                    response = self.ghost_post.create_post(button_url=url, content=content, title=title, tags=["경복궁"],
                                                           slug="GBG-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1

    def changdeokgung_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody"
        article_xpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[4]/td"
        attachment_xpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody/tr[5]/td/table/tbody/tr/td[3]/a"
        page = 1

        while True:
            self.driver.get(
                f"https://www.cdg.go.kr/cms_for_cdg/process/board/list.jsp?nowPage={page}&show_no=23&check_no=4&c_relation=48&c_relation2=110")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))
            for i in range(2, number_of_rows, 2):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return
                    title = self.driver.find_element(By.XPATH, row_path + "/td[2]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[2]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[4]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, size, link = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        link = url
                        filename = self.driver.find_element(By.XPATH, attachment_xpath).text
                        size = 0
                    self.driver.back()
                    response = self.ghost_post.create_post(button_url=url, content=content, title=title, tags=["창덕궁"],
                                                           slug="GBG-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1

    def changgyeonggung_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[2]/div[6]/div[2]/div[2]/div/div[2]/table/tbody/"
        article_xpath = "/html/body/div[2]/div[6]/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/div"
        attachment_xpath = "/html/body/div[2]/div[6]/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/dl[6]/dd/ul/li[1]/a"
        page = 1

        while True:
            self.driver.get(
                f"https://cgg.cha.go.kr/agapp/public/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000195&nttId=0&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&authFlag=&pageIndex={page}&pageNo=75040000&ctgoryId=&siteCd=CGG&searchBgnDe=&searchEndDe=&searchCnd=4&searchWrd=")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

            for i in range(1, number_of_rows + 1):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return

                    title = self.driver.find_element(By.XPATH, row_path + "/td[2]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[2]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[5]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, size, link = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        s = self.driver.find_element(By.XPATH, attachment_xpath).text
                        filename = s.split(" [")[0]
                        size = s.split(" [")[1].split(" byte]")[0]
                    self.driver.back()
                    response = self.ghost_post.create_post(button_url=url, content=content, title=title, tags=["창경궁"],
                                                           slug="CGG-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1

    def deoksugung_notice_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        article_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[3]/div/div"
        attachment_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/a"
        page = 1

        while True:
            self.driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=NOT")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

            for i in range(1, number_of_rows + 1):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return

                    title = self.driver.find_element(By.XPATH, row_path + "/td[2]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[2]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[3]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, link, size = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        link = self.driver.find_element(By.XPATH, attachment_xpath).get_attribute("href")
                        filename = self.driver.find_element(By.XPATH, attachment_xpath).text
                        size = self.driver.execute_script(
                            "return fetch(arguments[0], {method: 'HEAD'}).then(response => response.headers.get('content-length'));",
                            link)
                    self.driver.back()
                    response = self.ghost_post.create_post(button_url=url, content=content, title=title,
                                                           tags=["덕수궁", "덕수궁 공지"],
                                                           slug="DSUN-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1

    def deoksugung_career_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        article_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[3]/div/div"
        attachment_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/a"
        page = 1

        while True:
            self.driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=JOB")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

            for i in range(1, number_of_rows + 1):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return

                    title = self.driver.find_element(By.XPATH, row_path + "/td[2]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[2]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[3]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, link, size = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        link = self.driver.find_element(By.XPATH, attachment_xpath).get_attribute("href")
                        filename = self.driver.find_element(By.XPATH, attachment_xpath).text
                        size = self.driver.execute_script(
                            "return fetch(arguments[0], {method: 'HEAD'}).then(response => response.headers.get('content-length'));",
                            link)
                    self.driver.back()
                    response = self.ghost_post.create_post(button_url=url, content=content, title=title,
                                                           tags=["덕수궁", "덕수궁 채용"],
                                                           slug="DSUN-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1

    def deoksugung_event_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        article_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[3]/div/div"
        attachment_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/a"
        page = 1

        while True:
            self.driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=EVT")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

            for i in range(1, number_of_rows + 1):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return

                    title = self.driver.find_element(By.XPATH, row_path + "/td[2]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[2]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[3]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, link, size = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        link = self.driver.find_element(By.XPATH, attachment_xpath).get_attribute("href")
                        filename = self.driver.find_element(By.XPATH, attachment_xpath).text
                        size = self.driver.execute_script(
                            "return fetch(arguments[0], {method: 'HEAD'}).then(response => response.headers.get('content-length'));",
                            link)
                    self.driver.back()
                    response = self.ghost_post.create_post(button_url=url, content=content, title=title,
                                                           tags=["덕수궁", "덕수궁 행사"],
                                                           slug="DSUN-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1

    def jongmyo_event_fetch_until(self, until_id):
        bord_xpath = "/html/body/div[2]/div[3]/div[2]/div[2]/div/div[2]/table/tbody/"
        article_xpath = "/html/body/div[2]/div[3]/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/div"
        attachment_xpath = "/html/body/div[2]/div[3]/div[2]/div[2]/div/div[2]/form/div[1]/div[1]/dl[6]/dd/ul/li/a"
        page = 1

        while True:
            self.driver.get(
                f"https://jm.cha.go.kr/agapp/public/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000208&nttId=0&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&authFlag=&pageIndex={page}&pageNo=75030000&ctgoryId=&siteCd=JM&searchBgnDe=&searchEndDe=&searchCnd=4&searchWrd=")
            number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

            for i in range(1, number_of_rows + 1):
                row_path = bord_xpath + "/tr[" + str(i) + "]"

                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text

                if not article_id.isnumeric():
                    number_of_rows -= 1
                    continue
                else:
                    article_id = int(article_id)
                    if article_id <= until_id:
                        return

                    title = self.driver.find_element(By.XPATH, row_path + "/td[2]/a").text
                    url = self.driver.find_element(By.XPATH, row_path + "/td[2]/a")
                    date = self.driver.find_element(By.XPATH, row_path + "/td[5]").text

                    print(f"Fetching #{article_id}: {title}")

                    url.click()
                    url = self.driver.current_url
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, article_xpath)))
                    content = self.driver.find_element(By.XPATH, article_xpath).text
                    filename, size, link = None, None, None
                    if len(self.driver.find_elements(By.XPATH, attachment_xpath)) > 0:
                        s = self.driver.find_element(By.XPATH, attachment_xpath).text
                        filename = s.split(" [")[0]
                        size = s.split(" [")[1].split(" byte]")[0]
                    self.driver.back()

                    response = self.ghost_post.create_post(button_url=url, content=content, title=title, tags=["종묘"],
                                                           slug="CGG-" + str(article_id), string_time=date,
                                                           is_time_now=False,
                                                           filename=filename,
                                                           file_url=link, file_size=size)
                    print(f'Response: {response.status_code}')

            print(f"page: {page}, number of rows: {number_of_rows}")
            page += 1


if __name__ == '__main__':
    # Initialize the FetchUntil class with your admin API key
    admin_api_key = "your_admin_api_key_here"
    fetcher = FetchUntil(admin_api_key)

    # Define the article ID until which you want to fetch data
    until_id = 100  # Replace with the desired ID

    # Fetch data from different websites
    fetcher.gyeongbokgung_fetch_until(until_id)
    fetcher.changdeokgung_fetch_until(until_id)
    fetcher.changgyeonggung_fetch_until(until_id)
    fetcher.deoksugung_notice_fetch_until(until_id)
    fetcher.deoksugung_career_fetch_until(until_id)
    fetcher.deoksugung_event_fetch_until(until_id)
    fetcher.jongmyo_event_fetch_until(until_id)
