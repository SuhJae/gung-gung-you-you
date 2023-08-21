import jwt
import json
import requests
from datetime import datetime as date

class LastPostFetcher:
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

    def gyeongbokgung_get_last_id(self):
        tag = "gyeongbokgung"
        return self._get_last_id(tag)

    def changdeokgung_get_last_id(self):
        tag = "changdeokgung"
        return self._get_last_id(tag)

    def changgyeonggung_get_last_id(self):
        tag = "changgyeonggung"
        return self._get_last_id(tag)

    def deoksugung_notice_get_last_id(self):
        tag = "deoksugung-notice"
        return self._get_last_id(tag)

    def deoksugung_career_get_last_id(self):
        tag = "deoksugung-career"
        return self._get_last_id(tag)

    def deoksugung_event_get_last_id(self):
        tag = "deoksugung-event"
        return self._get_last_id(tag)

    def jongmyo_get_last_id(self):
        tag = "jongmyo"
        return self._get_last_id(tag)

    def _get_last_id(self, tag):
        url = f"{self.base_url}?filter=tag:{tag}&limit=1&order=updated_at%20desc"
        headers = {"Authorization": f"Ghost {self.token}"}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return int(data['posts'][0]['slug'].split('-')[1])

# Example usage:
if __name__ == "__main__":
    key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
    post_fetcher = LastPostFetcher(key)

    print(f'gyeongbokgung: {post_fetcher.gyeongbokgung_get_last_id()}')
    print(f'changdeokgung: {post_fetcher.changdeokgung_get_last_id()}')
    print(f'changgyeonggung: {post_fetcher.changgyeonggung_get_last_id()}')
    print(f'deoksugung-notice: {post_fetcher.deoksugung_notice_get_last_id()}')
    print(f'deoksugung-career: {post_fetcher.deoksugung_career_get_last_id()}')
    print(f'deoksugung-event: {post_fetcher.deoksugung_event_get_last_id()}')
    print(f'jongmyo: {post_fetcher.jongmyo_get_last_id()}')

