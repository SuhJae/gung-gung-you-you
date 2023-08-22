from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from lastpost import SourceLastID, GhostLastId
from datetime import datetime as date
from fetch import FetchUntil
from datetime import datetime
import random
import time

# make it look like human
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

options = Options()
options.add_argument("--headless")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

ko_key = "64e46446ea9500431950ab72:6a8326f4717aadf6ba86eddb55c37f6c01804afa5f63a560c557ae27b68ea98c"
en_key = "64e481321ccb164eaf726ba1:00f732b7317af964706964645ed249f63a2ecfa8f253047f8a4cc599e189a684"
ghost_last_id = GhostLastId(ko_key)
fetch_until = FetchUntil(ko_key, en_key, driver)
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


def check_update(max_retries = 5):
    print(f'[{datetime.now().strftime("%m/%d %H:%M:%S")}] Checking update')
    no_update = []

    def sync_with_retry(sync_func, ghost_func, source_func, name):
        retries = 0
        while retries < max_retries:
            try:
                if sync_func(ghost_func(), source_func(), name):
                    return True
                else:
                    return False
            except Exception as e:
                print(f"An error occurred during sync for {name}: {e}.\nRetrying... ({retries + 1}/{max_retries})")
                retries += 1
                time.sleep(1)
        return False

    if not sync_with_retry(sync, ghost_last_id.gyeongbokgung, source_last_id.gyeongbokgung, '경복궁'):
        no_update.append('경복궁')
    if not sync_with_retry(sync, ghost_last_id.changdeokgung, source_last_id.changdeokgung, '창덕궁'):
        no_update.append('창덕궁')
    if not sync_with_retry(sync, ghost_last_id.changgyeonggung, source_last_id.changgyeonggung, '창경궁'):
        no_update.append('창경궁')
    if not sync_with_retry(sync, ghost_last_id.deoksugung_notice, source_last_id.deoksugung_notice, '덕수궁-공지'):
        no_update.append('덕수궁-공지')
    if not sync_with_retry(sync, ghost_last_id.deoksugung_career, source_last_id.deoksugung_career, '덕수궁-채용'):
        no_update.append('덕수궁-채용')
    if not sync_with_retry(sync, ghost_last_id.deoksugung_event, source_last_id.deoksugung_event, '덕수궁-행사'):
        no_update.append('덕수궁-행사')
    if not sync_with_retry(sync, ghost_last_id.jongmyo, source_last_id.jongmyo, '종묘'):
        no_update.append('종묘')

    if len(no_update) != 0:
        print(f'[{datetime.now().strftime("%m/%d %H:%M:%S")}] No update on: {", ".join(no_update)}')


if __name__ == '__main__':
    check_update(1)
    while True:
        random_time = random.randint(60, 120) # to make it look like human
        print(f'[{date.now().strftime("%m/%d %H:%M:%S")}] Waiting for {random_time} seconds')
        time.sleep(random_time)
        check_update(5)
