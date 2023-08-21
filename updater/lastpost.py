from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import jwt
import json
import requests
from datetime import datetime as date


class GhostLastId:
    def __init__(self, key):
        self.adminId, self.secret = key.split(":")
        self.token = self.generate_token()
        self.base_url = "https://gung.joseon.space/ghost/api/admin/posts/"

    def generate_token(self):
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.adminId}
        payload = {
            "iat": iat,
            "exp": iat + 5 * 60,
            "aud": "/admin/"
        }
        return jwt.encode(payload, bytes.fromhex(self.secret), algorithm="HS256", headers=header)

    def gyeongbokgung(self):
        tag = "gyeongbokgung"
        return self._get_last_id(tag)

    def changdeokgung(self):
        tag = "changdeokgung"
        return self._get_last_id(tag)

    def changgyeonggung(self):
        tag = "changgyeonggung"
        return self._get_last_id(tag)

    def deoksugung_notice(self):
        tag = "deoksugung-notice"
        return self._get_last_id(tag)

    def deoksugung_career(self):
        tag = "deoksugung-career"
        return self._get_last_id(tag)

    def deoksugung_event(self):
        tag = "deoksugung-event"
        return self._get_last_id(tag)

    def jongmyo(self):
        tag = "jongmyo"
        return self._get_last_id(tag)

    def _get_last_id(self, tag):
        url = f"{self.base_url}?filter=tag:{tag}&limit=1&order=updated_at%20desc"
        headers = {"Authorization": f"Ghost {self.token}"}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return int(data['posts'][0]['slug'].split('-')[1])

class SourceLastID:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--blink-settings=imagesEnabled=false")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def gyeongbokgung(self, page = 1):
        bord_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/form/div/table/tbody"
        self.driver.get(f"https://www.royalpalace.go.kr/content/board/list.asp?page={page}")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/th").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def changdeokgung(self, page = 1):
        bord_xpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody"
        self.driver.get(f"https://www.cdg.go.kr/cms_for_cdg/process/board/list.jsp?nowPage={page}&show_no=23&check_no=4&c_relation=48&c_relation2=110")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def changgyeonggung(self, page = 1):
        bord_xpath = "/html/body/div[2]/div[6]/div[2]/div[2]/div/div[2]/table/tbody/"
        self.driver.get(f"https://cgg.cha.go.kr/agapp/public/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000195&nttId=0&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&authFlag=&pageIndex={page}&pageNo=75040000&ctgoryId=&siteCd=CGG&searchBgnDe=&searchEndDe=&searchCnd=4&searchWrd=")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def deoksugung_notice(self, page = 1):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        self.driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=NOT")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def deoksugung_career(self, page = 1):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        self.driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=JOB")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def deoksugung_event(self, page = 1):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        self.driver.get(f"https://www.deoksugung.go.kr/board/list?page={page}&board_id=EVT")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def jongmyo(self, page = 1):
        bord_xpath = "/html/body/div[2]/div[3]/div[2]/div[2]/div/div[2]/table/tbody/"
        self.driver.get(f"https://jm.cha.go.kr/agapp/public/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000208&nttId=0&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&authFlag=&pageIndex={page}&pageNo=75030000&ctgoryId=&siteCd=JM&searchBgnDe=&searchEndDe=&searchCnd=4&searchWrd=")
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + "/tr[" + str(i) + "]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + "/td[1]").text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id


# Example usage:
if __name__ == "__main__":
    key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
    ghost_last_id = GhostLastId(key)
    source_last_id = SourceLastID()

    print("Ghost Last ID".center(30, "="))
    print(f'gyeongbokgung: {ghost_last_id.gyeongbokgung()}')
    print(f'changdeokgung: {ghost_last_id.changdeokgung()}')
    print(f'changgyeonggung: {ghost_last_id.changgyeonggung()}')
    print(f'deoksugung-notice: {ghost_last_id.deoksugung_notice()}')
    print(f'deoksugung-career: {ghost_last_id.deoksugung_career()}')
    print(f'deoksugung-event: {ghost_last_id.deoksugung_event()}')
    print(f'jongmyo: {ghost_last_id.jongmyo()}')
    print("="*30 + "\n")

    print("Source Last ID".center(30, "="))
    print(f'gyeongbokgung: {source_last_id.gyeongbokgung()}')
    print(f'changdeokgung: {source_last_id.changdeokgung()}')
    print(f'changgyeonggung: {source_last_id.changgyeonggung()}')
    print(f'deoksugung-notice: {source_last_id.deoksugung_notice()}')
    print(f'deoksugung-career: {source_last_id.deoksugung_career()}')
    print(f'deoksugung-event: {source_last_id.deoksugung_event()}')
    print(f'jongmyo: {source_last_id.jongmyo()}')
    print("="*30 + "\n")

