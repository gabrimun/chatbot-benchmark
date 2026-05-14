import requests

# Config
BASE_URL = "http://127.0.0.1"
PORT = "5050"
ENDPOINT = "/api/response"  

# URL
url = f"{BASE_URL}:{PORT}{ENDPOINT}"

response = requests.get(url)

payload = {"query": "Dove devo cliccare per inserire un nuovo cliente nel sistema?",
            "role": "backoffice",
            "dev": "false"}
response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print("Successo:", data)
else:
    print(f"Errore {response.status_code}: {response.text}")