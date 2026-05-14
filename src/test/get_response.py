import requests
import csv
import time
import re

# Config
BASE_URL = "http://127.0.0.1"
PORT = "5050"
ENDPOINT = "/api/response"  

# URL
url = f"{BASE_URL}:{PORT}{ENDPOINT}"

response = requests.get(url)

with open('questions.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:

        payload = {"query": row['domande'],
                    "role": row['ruolo'],
                    "dev": "false"}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result")

            result = result.split("Puoi consultare")[0].strip()

            print(result)
        else:
            print(f"Errore {response.status_code}: {response.text}")

        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break