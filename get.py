import jwt
import json
import requests
from datetime import datetime as date

# Admin API key goes here
key = "64e46446ea9500431950ab72:6a8326f4717aadf6ba86eddb55c37f6c01804afa5f63a560c557ae27b68ea98c"

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

# slug = input("Enter slug or press enter for recent post: ")
slug = ""


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

    # Save the mobile doc as a JSON file
    with open(json_filename, "w") as json_file:
        # turn the mobiledoc string into a dictionary
        mobile_doc = json.loads(data["posts"][0]["mobiledoc"])
        # save the mobiledoc dictionary as a JSON file which is easier to read
        json.dump(mobile_doc, json_file, indent=4)


    print(f"Data saved as {json_filename}")
else:
    print(f"Request failed with status code {response.status_code}")