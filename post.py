import requests
import jwt
import json
from datetime import datetime as date

class GhostPost:
    def __init__(self, admin_key):
        self.admin_id, self.secret = admin_key.split(":")
        self.header = {"alg": "HS256", "typ": "JWT", "kid": self.admin_id}
        self.url = "https://gung.joseon.space/ghost/api/admin/posts/"

    def generate_token(self):
        iat = int(date.now().timestamp())
        payload = {
            "iat": iat,
            "exp": iat + 5 * 60,
            "aud": "/admin/"
        }
        token = jwt.encode(payload, bytes.fromhex(self.secret), algorithm="HS256", headers=self.header)
        return token

    def create_post(self, button_url, content, title, tags, slug, string_time, is_time_now, filename, file_url, file_size):
        with requests.Session() as session:
            token = self.generate_token()

            if is_time_now:
                date_str = date.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            else:
                date_obj = date.strptime(string_time, "%Y-%m-%d")
                date_str = date_obj.replace(hour=3, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S.000Z")

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
                    "fileTitle": "첨부파일",
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
                        "buttonText": "원문 보기",
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

            headers = {"Authorization": f"Ghost {token}"}
            response = session.post(self.url, json=body, headers=headers)

        return response


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


