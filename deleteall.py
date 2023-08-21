import requests
import jwt
import json
from datetime import datetime as date

# Admin API key goes here
key = "64e046244c86ecf011c46ad4:a12be87aabbbf7a5b1def014d78688bc577930df0ed09547342de13396336e0c"

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

# Make an authenticated request to create a post

delete_tag = "deoksugung-event"

# filter: &filter=visibility:public

url = f"https://gung.joseon.space/ghost/api/admin/posts/?filter=tag:{delete_tag}&limit=all"

headers = {"Authorization": "Ghost {}".format(token)}


r = requests.get(url, headers=headers)
data = r.json()


for post in data['posts']:
    print(f"Deleting {post['title']}...")

    post_id = post['id']
    delete_url = f'https://gung.joseon.space/ghost/api/admin/posts/{post_id}/'
    r = requests.delete(delete_url, headers=headers)
    print(f"Data deleted: {post_id}")
