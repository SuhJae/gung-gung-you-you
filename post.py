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

    def create_post(self):
        with requests.Session() as session:
            token = self.generate_token()
            date_str = date.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

            with open ('doc.json', 'r') as f:
                mobile_doc = json.load(f)

            mobile_doc = json.dumps(mobile_doc)

            body = {
                "posts": [{
                    "title": "Json Test Post",
                    "status": "draft",
                    "published_at": date_str,
                    "updated_at": date_str,
                    "mobiledoc": mobile_doc,
                }]
            }

            headers = {"Authorization": f"Ghost {token}"}
            response = session.post(self.url, json=body, headers=headers)

        return response


# Example usage:
if __name__ == "__main__":
    admin_api_key = "64e46446ea9500431950ab72:6a8326f4717aadf6ba86eddb55c37f6c01804afa5f63a560c557ae27b68ea98c"
    ghost_post = GhostPost(admin_api_key)

    response = ghost_post.create_post()
    print(response.status_code)

    # get the post and save it as a json file


