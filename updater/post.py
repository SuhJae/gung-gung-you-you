import requests
import jwt
import json
import translators as ts
from datetime import datetime as date

class GhostPost:
    def __init__(self, admin_key, en_key):
        self.admin_id, self.secret = admin_key.split(":")
        self.header = {"alg": "HS256", "typ": "JWT", "kid": self.admin_id}
        self.url = "https://gung.joseon.space/ghost/api/admin/posts/"
        self.token, self.token_exp = self.generate_token()

        self.en_id, self.en_secret = en_key.split(":")
        self.en_header = {"alg": "HS256", "typ": "JWT", "kid": self.en_id}
        self.en_url = "https://en.gung.joseon.space/ghost/api/admin/posts/"
        self.en_token, self.en_token_exp = self.generate_token_en()

        self.tag_dict = {'경복궁':'gyeongbokgung', '덕수궁': 'deoksugung', '창덕궁': 'changdeokgung',
                         '창경궁': 'changgyeonggung', '종묘': 'jongmyo', '덕수궁 공지': 'deoksugung-notice',
                        '덕수궁 채용': 'deoksugung-career', '덕수궁 행사': 'deoksugung-event'}

    def generate_token(self):
        iat = int(date.now().timestamp())
        payload = {
            "iat": iat,
            "exp": iat + 5 * 60,
            "aud": "/admin/"
        }
        token = jwt.encode(payload, bytes.fromhex(self.secret), algorithm="HS256", headers=self.header)
        return token, payload['exp']

    def generate_token_en(self):
        iat = int(date.now().timestamp())
        payload = {
            "iat": iat,
            "exp": iat + 5 * 60,
            "aud": "/admin/"
        }
        token = jwt.encode(payload, bytes.fromhex(self.en_secret), algorithm="HS256", headers=self.en_header)
        return token, payload['exp']

    def create_post(self, button_url, content, title, tags, slug, string_time, is_time_now, filename, file_url, file_size):
        if date.now().timestamp() > self.token_exp:
            print("Token expired. Generating new token...")
            self.token, self.token_exp = self.generate_token()
        if date.now().timestamp() > self.en_token_exp:
            print("Token expired. Generating new token...")
            self.en_token, self.en_token_exp = self.generate_token_en()

        token = self.token
        en_token = self.en_token

        if is_time_now:
            date_str = date.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        else:
            date_obj = date.strptime(string_time, "%Y-%m-%d")
            date_str = date_obj.replace(hour=3, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # ====================================
        # this is for posting in Korean
        # ====================================

        formatted_mobile_doc = self.create_mobile_doc(content, filename, file_url, file_size, "첨부파일", "원문 보기", button_url)

        body = {
            "posts": [{
                "title": title,
                "tags": tags,
                "status": "published",
                "published_at": date_str,
                "updated_at": date_str,
                "mobiledoc": formatted_mobile_doc,
                "slug": slug
            }]
        }

        headers = {"Authorization": f"Ghost {token}"}
        response = requests.post(self.url, headers=headers, json=body)

        if response.status_code != 201:
            print(f'Exception {response.status_code} occured while posting in Korean: {response.text}')
        else:
            print(f'Successfully posted in Korean ({slug})')

        # ====================================
        # this is for posting in English
        # ====================================

        # try translation 5 times
        for i in range(5):
            try:
                content = (ts.translate_text(query_text=content, target_lang="en", source_lang="ko", translator='papago'))
                title = (ts.translate_text(query_text=title, target_lang="en", source_lang="ko", translator='papago'))
                break
            except Exception:
                print(f'Exception occured while translating ({i+1}/5)')
                if i == 4:
                    print('Failed to translate. Saving details into CSV for manual translation.')
                    with open('failed_translation.csv', 'a', encoding='utf-8') as f:
                        f.write(f'{slug}, {title}, {button_url}\n')

        formatted_mobile_doc = self.create_mobile_doc(content, filename, file_url, file_size, "Attachment File", "View Original Post", button_url)
        tags = [self.tag_dict[tag] for tag in tags]

        body = {
            "posts": [{
                "title": title,
                "tags": tags,
                "status": "published",
                "published_at": date_str,
                "updated_at": date_str,
                "mobiledoc": formatted_mobile_doc,
                "slug": slug
            }]
        }

        headers = {"Authorization": f"Ghost {en_token}"}
        response = requests.post(self.en_url, headers=headers, json=body)

        if response.status_code != 201:
            print(f'Exception {response.status_code} occured while posting in English: {response.text}')
        else:
            print(f'Successfully posted in English ({slug})')

        return response

    def create_mobile_doc(self, content, filename, file_url, file_size, file_title, button_text, button_url):
        content_lines = content.split('\n')
        paragraph_items = []

        for line in content_lines:
            paragraph_items.append([1, "p", [[0, [], 0, line.strip()]]])

        paragraph_items.append([10, 0])
        paragraph_items.append([10, 1])
        paragraph_items.append([10, 2])

        if filename is not None and file_url is not None and file_size is not None:
            filestring = {
                "loop": False,
                "src": file_url,
                "fileName": filename,
                "fileTitle": file_title,
                "fileCaption": "",
                "fileSize": file_size
            }
        else:
            filestring = None

        mobile_doc = {
            "version": "0.3.1",
            "atoms": [],
            "cards": [
                ["file", filestring] if filestring is not None else [],
                ["hr", {}],
                ["button", {
                    "alignment": "center",
                    "buttonText": button_text,
                    "buttonUrl": button_url
                }]
            ],
            "markups": [],
            "sections": paragraph_items,
            "ghostVersion": "4.0"
        }
        return json.dumps(mobile_doc, indent=4)


# Example usage:
if __name__ == "__main__":
    admin_api_key = ""
    ghost_post = GhostPost(admin_api_key)

    button_url = ""
    content = ""
    title = ""
    tags = ["경복궁"]
    slug = ""
    string_time = "2023-08-19"
    is_time_now = False

    response = ghost_post.create_post(button_url, content, title, tags, slug, string_time, is_time_now)
    print(response)


