from faker import Faker

fake = Faker()

import requests
import json

url = "http://127.0.0.1:5000/users"

for i in range(100):
    payload = json.dumps({
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password()
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
