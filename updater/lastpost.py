import jwt
import json
import requests
from datetime import datetime as date

class LastId:
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

# Example usage:
if __name__ == "__main__":
    key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"
    last_id = LastId(key)

    print(f'gyeongbokgung: {last_id.gyeongbokgung()}')
    print(f'changdeokgung: {last_id.changdeokgung()}')
    print(f'changgyeonggung: {last_id.changgyeonggung()}')
    print(f'deoksugung-notice: {last_id.deoksugung_notice()}')
    print(f'deoksugung-career: {last_id.deoksugung_career()}')
    print(f'deoksugung-event: {last_id.deoksugung_event()}')
    print(f'jongmyo: {last_id.jongmyo()}')
