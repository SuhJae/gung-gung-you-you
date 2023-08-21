from datetime import datetime as date

import jwt

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
