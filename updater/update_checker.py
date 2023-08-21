from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from lastpost import SourceLastID, GhostLastId
from datetime import datetime as date
from fetch import FetchUntil
import time
import random

# make it look like human
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

options = Options()
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
ghost_last_id = GhostLastId(key)
fetch_until = FetchUntil(key, driver)
source_last_id = SourceLastID(driver)

print('Setup Finished')


def sync(ghost, source, name):
    if ghost == source:
        return False
    print(f'There is new update on {name} that is not crawled. {ghost}/{source}')
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
    print(f'[{date.now().strftime("%m/%d %H:%M:%S")}] Checking update')
    no_update = []

    if not sync(ghost_last_id.gyeongbokgung(), source_last_id.gyeongbokgung(), '경복궁'):
        no_update.append('경복궁')
    if not sync(ghost_last_id.changdeokgung(), source_last_id.changdeokgung(), '창덕궁'):
        no_update.append('창덕궁')
    if not sync(ghost_last_id.changgyeonggung(), source_last_id.changgyeonggung(), '창경궁'):
        no_update.append('창경궁')
    if not sync(ghost_last_id.deoksugung_notice(), source_last_id.deoksugung_notice(), '덕수궁-공지'):
        no_update.append('덕수궁-공지')
    if not sync(ghost_last_id.deoksugung_career(), source_last_id.deoksugung_career(), '덕수궁-채용'):
        no_update.append('덕수궁-채용')
    if not sync(ghost_last_id.deoksugung_event(), source_last_id.deoksugung_event(), '덕수궁-행사'):
        no_update.append('덕수궁-행사')
    if not sync(ghost_last_id.jongmyo(), source_last_id.jongmyo(), '종묘'):
        no_update.append('종묘')

    if len(no_update) != 0:
        print(f'[{date.now().strftime("%m/%d %H:%M:%S")}] No update on: {", ".join(no_update)}')


if __name__ == '__main__':
    check_update()
    while True:
        random_time = random.randint(60, 120) # to make it look like human
        print(f'[{date.now().strftime("%m/%d %H:%M:%S")}] Waiting for {random_time} seconds')
        time.sleep(random_time)
        check_update()
