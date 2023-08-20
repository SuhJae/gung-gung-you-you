import jwt
import json
import requests
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

slug = input("Enter slug or press enter for recent post: ")


# Create the token (including decoding secret)
token = jwt.encode(payload, bytes.fromhex(secret), algorithm="HS256", headers=header)

if slug == "":
    url = "https://gung.joseon.space/ghost/api/admin/posts/"
else:
    url = "https://gung.joseon.space/ghost/api/admin/posts/slug/" + slug + "/"


headers = {"Authorization": "Ghost {}".format(token)}

response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response content into a Python dictionary
    data = json.loads(response.text)

    # Define the name of the JSON file where you want to save the data
    json_filename = "response_data.json"

    # Save the data as a JSON file
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data saved as {json_filename}")
else:
    print(f"Request failed with status code {response.status_code}")