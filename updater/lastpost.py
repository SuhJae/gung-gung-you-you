from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import jwt
import time
import json
import requests
from datetime import datetime as date


class GhostLastId:
    def __init__(self, key):
        self.adminId, self.secret = key.split(":")
        self.token, self.token_exp = self.generate_token()
        self.base_url = "https://gung.joseon.space/ghost/api/admin/posts/"

    def generate_token(self):
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.adminId}
        payload = {
            "iat": iat,
            "exp": iat + 60 * 5, # 5 minutes expiration
            "aud": "/admin/"
        }
        return jwt.encode(payload, bytes.fromhex(self.secret), algorithm="HS256", headers=header), payload['exp']

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

    def _get_last_id(self, tag, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                if date.now().timestamp() > self.token_exp:
                    print("Token expired. Generating new token...")
                    self.token, self.token_exp = self.generate_token()
                url = f"{self.base_url}?filter=tag:{tag}&limit=1&order=updated_at%20desc"
                headers = {"Authorization": f"Ghost {self.token}"}
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for bad responses

                data = json.loads(response.text)
                return int(data['posts'][0]['slug'].split('-')[1])
            except (requests.RequestException, json.JSONDecodeError) as e:
                print(f"An error occurred during fetcing last article of {tag}: {e}.\nRetrying... ({retries + 1}/{max_retries})")
                retries += 1
                time.sleep(1)

        raise Exception(f"Failed after {max_retries} retries")


class SourceLastID:
    def __init__(self, driver=None):
        if driver is None:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--blink-settings=imagesEnabled=false")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        else:
            self.driver = driver

    def get_last_article_id(self, bord_xpath, url, page=1, column="/td[1]"):
        self.driver.get(url.format(page=page))
        number_of_rows = len(self.driver.find_elements(By.XPATH, bord_xpath + "/tr"))

        last_article_id = 0
        for i in range(1, number_of_rows + 1):
            row_path = bord_xpath + f"/tr[{i}]"
            try:
                article_id = self.driver.find_element(By.XPATH, row_path + column).text
            except:
                continue
            if not article_id.isnumeric():
                continue
            if int(article_id) > last_article_id:
                last_article_id = int(article_id)

        return last_article_id

    def gyeongbokgung(self, page=1):
        bord_xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/form/div/table/tbody"
        url = "https://www.royalpalace.go.kr/content/board/list.asp?page={page}"
        return self.get_last_article_id(bord_xpath, url, page, "/th")

    def changdeokgung(self, page=1):
        bord_xpath = "/html/body/div[1]/div[4]/b/div/div[2]/center/table/tbody"
        url = "https://www.cdg.go.kr/cms_for_cdg/process/board/list.jsp?nowPage={page}&show_no=23&check_no=4&c_relation=48&c_relation2=110"
        return self.get_last_article_id(bord_xpath, url, page)

    def changgyeonggung(self, page=1):
        bord_xpath = "/html/body/div[2]/div[6]/div[2]/div[2]/div/div[2]/table/tbody/"
        url = "https://cgg.cha.go.kr/agapp/public/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000195&nttId=0&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&authFlag=&pageIndex={page}&pageNo=75040000&ctgoryId=&siteCd=CGG&searchBgnDe=&searchEndDe=&searchCnd=4&searchWrd="
        return self.get_last_article_id(bord_xpath, url, page)

    def deoksugung_notice(self, page=1):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        url = "https://www.deoksugung.go.kr/board/list?page={page}&board_id=NOT"
        return self.get_last_article_id(bord_xpath, url, page)

    def deoksugung_career(self, page=1):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        url = "https://www.deoksugung.go.kr/board/list?page={page}&board_id=JOB"
        return self.get_last_article_id(bord_xpath, url, page)

    def deoksugung_event(self, page=1):
        bord_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/div[2]/div/div/div/div[2]/table/tbody/"
        url = "https://www.deoksugung.go.kr/board/list?page={page}&board_id=EVT"
        return self.get_last_article_id(bord_xpath, url, page)

    def jongmyo(self, page=1):
        bord_xpath = "/html/body/div[2]/div[3]/div[2]/div[2]/div/div[2]/table/tbody/"
        url = "https://jm.cha.go.kr/agapp/public/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000208&nttId=0&bbsTyCode=BBST03&bbsAttrbCode=BBSA03&authFlag=&pageIndex={page}&pageNo=75030000&ctgoryId=&siteCd=JM&searchBgnDe=&searchEndDe=&searchCnd=4&searchWrd="
        return self.get_last_article_id(bord_xpath, url, page)


# Example usage:
if __name__ == "__main__":
    key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
    ghost_last_id = GhostLastId(key)
    source_last_id = SourceLastID()
    while True:

        print("Ghost Last ID".center(30, "="))
        print(f'gyeongbokgung: {ghost_last_id.gyeongbokgung()}')
        print(f'changdeokgung: {ghost_last_id.changdeokgung()}')
        print(f'changgyeonggung: {ghost_last_id.changgyeonggung()}')
        print(f'deoksugung-notice: {ghost_last_id.deoksugung_notice()}')
        print(f'deoksugung-career: {ghost_last_id.deoksugung_career()}')
        print(f'deoksugung-event: {ghost_last_id.deoksugung_event()}')
        print(f'jongmyo: {ghost_last_id.jongmyo()}')
        print("="*30 + "\n")

        # print("Source Last ID".center(30, "="))
        # print(f'gyeongbokgung: {source_last_id.gyeongbokgung()}')
        # print(f'changdeokgung: {source_last_id.changdeokgung()}')
        # print(f'changgyeonggung: {source_last_id.changgyeonggung()}')
        # print(f'deoksugung-notice: {source_last_id.deoksugung_notice()}')
        # print(f'deoksugung-career: {source_last_id.deoksugung_career()}')
        # print(f'deoksugung-event: {source_last_id.deoksugung_event()}')
        # print(f'jongmyo: {source_last_id.jongmyo()}')
        # print("="*30 + "\n")

        time.sleep(30)

