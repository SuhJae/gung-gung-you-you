import jwt
import time
import json
import requests
from datetime import datetime as date
import translators as ts
# import deepl


class Migration:
    def __init__(self, from_key, to_key, deepL_key):
        # self.translator = deepl.Translator(deepL_key)
        self.from_adminId, self.from_secret = from_key.split(":")
        self.from_token, self.from_token_exp = self.generate_from_token()
        self.from_base_url = "https://gung.joseon.space/ghost/api/admin/posts/"

        self.to_adminId, self.to_secret = to_key.split(":")
        self.to_token, self.to_token_exp = self.generate_to_token()
        self.to_base_url = "https://en.gung.joseon.space/ghost/api/admin/posts/"

    def translate(self, text):
        services = ['papago', 'papago', 'papago', 'papago']

        for translator in services:
            try:
                result = ts.translate_text(query_text=text, target_lang="en", source_lang="ko", translator=translator)
                print(f"Translated using {translator}... (length: {len(text)})")
                return result
            except Exception:
                print(f"{translator} Error. Trying next service...")
                continue

        raise Exception("All translation services failed.")

    def generate_from_token(self):
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.from_adminId}
        payload = {
            "iat": iat,
            "exp": iat + 60 * 5, # 5 minutes expiration
            "aud": "/admin/"
        }
        return jwt.encode(payload, bytes.fromhex(self.from_secret), algorithm="HS256", headers=header), payload['exp']

    def generate_to_token(self):
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.to_adminId}
        payload = {
            "iat": iat,
            "exp": iat + 60 * 5, # 5 minutes expiration
            "aud": "/admin/"
        }
        return jwt.encode(payload, bytes.fromhex(self.to_secret), algorithm="HS256", headers=header), payload['exp']

    def count_posts(self):
        if date.now().timestamp() > self.from_token_exp:
            print("Token expired. Generating new token...")
            self.from_token, self.from_token_exp = self.generate_from_token()

        url = f'https://gung.joseon.space/ghost/api/admin/posts/?limit=all'
        response = requests.get(url, headers={"Authorization": f"Ghost {self.from_token}"})
        return len(json.loads(response.text)['posts'])


    def get_post(self, page):
        if date.now().timestamp() > self.from_token_exp:
            print("Token expired. Generating new token...")
            self.from_token, self.from_token_exp = self.generate_from_token()


        url = f'{self.from_base_url}?page={page}&limit=1&order=updated_at%20desc&order=title%20asc'
        response = requests.get(url, headers={"Authorization": f"Ghost {self.from_token}"})
        title = json.loads(response.text)['posts'][0]['title']
        print(f'[{page}] {title}')

        mobiledoc = json.loads(response.text)['posts'][0]['mobiledoc']
        mobiledoc = json.loads(mobiledoc)
        button_url = mobiledoc['cards'][2][1]['buttonUrl']
        sections = mobiledoc['sections']
        content = '\n'.join([item[2][0][3] for item in sections if item[1] == 'p'])

        file_info = mobiledoc.get('cards', [])[0]
        if file_info and file_info[0] == 'file':
            filename = file_info[1].get('fileName')
            file_url = file_info[1].get('src')
            file_size = file_info[1].get('fileSize')
        else:
            filename = None
            file_url = None
            file_size = None

        tags = json.loads(response.text)['posts'][0]['tags']
        tags = [tag['slug'] for tag in tags]
        slug = json.loads(response.text)['posts'][0]['slug']
        update_time = json.loads(response.text)['posts'][0]['updated_at']

        # Translate ko -> en-US
        if title != "":
            title = self.translate(title)
        if content != "":
            content = self.translate(content)

        response = self.create_post(button_url=button_url, content=content, title=title, tags=tags, slug=slug,
                                    time=update_time, filename=filename, file_url=file_url, file_size=file_size)
        if response.status_code == 201:
            print(f'Successfully migrated {title} ({page})')
        else:
            print(f'Error migrating {title} ({page})')
            with open("error.csv", "a") as f:
                f.write(f'{page},{title}\n')

        with open("progress.txt", "w") as f:
            f.write(str(page))

    def create_post(self, button_url, content, title, tags, slug, time, filename, file_url, file_size):
        if date.now().timestamp() > self.to_token_exp:
            print("Token expired. Generating new token...")
            self.to_token, self.to_token_exp = self.generate_to_token()

        # check if post already exists (with slug)
        url = f'{self.to_base_url}?filter=slug:{slug}'


        date_str = time
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
                "fileTitle": "Attachment File",
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
                    "buttonText": "View Original Post",
                    "buttonUrl": button_url
                }]
            ],
            "markups": [],
            "sections": paragraph_items,
            "ghostVersion": "4.0"
        }
        formatted_mobile_doc = json.dumps(mobile_doc, indent=4)

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

        headers = {"Authorization": f"Ghost {self.to_token}"}
        response = requests.post(self.to_base_url, headers=headers, json=body)
        return response


if __name__ == "__main__":
    from_key = "64e46446ea9500431950ab72:890ce30138c23149213a235fe6c6fdbfad92c12ea54f33d30c8bd5c4756e0e34"
    to_key = "64e358948b573504974e8082:641e78ee77152562b89ac4910f1c0c3f4ab53276165863db004ba525eca0d5fc"
    deepL_key = "e696d34b-262a-e2fe-9aa0-b1577eec98a7:fx"
    migration = Migration(from_key, to_key, deepL_key)

    # last_page = migration.count_posts()
    # print(f"Total posts: {last_page}")

    with open("progress.txt", "r") as f:
        last_page = int(f.read())
        last_page += 1

    print(f"Starting from {last_page}...")

    for i in range(last_page, 4115):
        migration.get_post(i)

