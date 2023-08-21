import requests
import jwt
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as date

# Admin API key goes here
key = "64e358948b573504974e8082:641e78ee77152562b89ac4910f1c0c3f4ab53276165863db004ba525eca0d5fc"

# Split the key into ID and SECRET
adminId, secret = key.split(":")

# Prepare header and payload
iat = int(date.now().timestamp())

header = {"alg": "HS256", "typ": "JWT", "kid": adminId}
payload = {
    "iat": iat,
    "exp": iat + 5 * 60,
    "aud": "/admin/"
}

# Create the token (including decoding secret)
token = jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)

delete_tag = "deoksugung-event"
base_url = "https://en.gung.joseon.space/ghost/api/admin/posts/"

headers = {"Authorization": "Ghost {}".format(token)}

def delete_post(post):
    post_id = post['id']
    delete_url = f'{base_url}{post_id}/'
    for _ in range(5):  # Retry up to 5 times
        try:
            r = requests.delete(delete_url, headers=headers)
            r.raise_for_status()  # Raise an exception for 4xx and 5xx errors
            print(f"Data deleted: {post['title']} (ID: {post_id})")
            break  # Success, exit retry loop
        except requests.exceptions.RequestException as e:
            print(f"Error deleting {post['title']} (ID: {post_id}): {e}")
    else:
        print(f"Max retries reached for {post['title']} (ID: {post_id})")

# Fetch data from the API
url = f"{base_url}?limit=all"
r = requests.get(url, headers=headers)
data = r.json()

# Parallelize the delete requests
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(delete_post, data['posts'])
