from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from lastpost import SourceLastID, GhostLastId
from fetch import FetchUntil
import schedule

options = Options()
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
ghost_last_id = GhostLastId(key)
fetch_until = FetchUntil(key, driver)
source_last_id = SourceLastID(driver)

print('Setup Finished')


def sync(ghost, source, name):
    if ghost == source:
        print(f'There is no update on {name}.')
        return False
    else:
        print(f'There is new update on {name} that is not crawled. {ghost} | {source}')
        print("Start crawling".center(30, '='))

        if name == '경복궁':
            fetch_until.gyeongbokgung(until_id=ghost)
        if name == '창덕궁':
            fetch_until.changdeokgung(until_id=ghost)
        if name == '창경궁':
            fetch_until.changgyeonggung(until_id=ghost)
        if name == '덕수궁-공지':
            fetch_until.deoksugung_notice(until_id=ghost)
        if name == '덕수궁-채용':
            fetch_until.deoksugung_career(until_id=ghost)
        if name == '덕수궁-행사':
            fetch_until.deoksugung_event(until_id=ghost)
        if name == '종묘':
            fetch_until.jongmyo(until_id=ghost)

        print("Crawling finished".center(30, '='))
        return True


def check_update():
    sync(ghost_last_id.gyeongbokgung(), source_last_id.gyeongbokgung(), '경복궁')
    sync(ghost_last_id.changdeokgung(), source_last_id.changdeokgung(), '창덕궁')
    sync(ghost_last_id.changgyeonggung(), source_last_id.changgyeonggung(), '창경궁')
    sync(ghost_last_id.deoksugung_notice(), source_last_id.deoksugung_notice(), '덕수궁-공지')
    sync(ghost_last_id.deoksugung_career(), source_last_id.deoksugung_career(), '덕수궁-채용')
    sync(ghost_last_id.deoksugung_event(), source_last_id.deoksugung_event(), '덕수궁-행사')
    sync(ghost_last_id.jongmyo(), source_last_id.jongmyo(), '종묘')


check_update()
