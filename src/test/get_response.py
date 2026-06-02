"""
GET_RESPONSE.PY - Chatbot Benchmark Execution & Local Embedding Generation

This script automates the benchmarking phase. It reads the questions dataset,
forwards HTTP POST requests to the local chatbot endpoint.

ROLE-DEPENDENCY WARNING:
This script is strictly tailored for a role-based chatbot architecture. The HTTP payload 
explicitly includes a "role" key, and responses are checked against role-specific patterns.

Modify the payload according to your chatbot implementation.
"""

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import pandas as pd
import requests
import time
import re
import os
import json
import argparse

load_dotenv()

# parser configuration
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, help="llm model name")
args = parser.parse_args()

# embedding model configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")

if not EMBEDDING_MODEL:
    raise RuntimeError("EMBEDDING_MODEL is not set. Check your .env file or environment.")


# Config chatbot url
BASE_URL = "http://127.0.0.1"
PORT = "5050"
ENDPOINT = "/api/response"  

# URL
url = f"{BASE_URL}:{PORT}{ENDPOINT}"

response = requests.get(url)

# error counters
chatbot_erros = 0

# model loading
model = SentenceTransformer(
    EMBEDDING_MODEL,
    device=EMBEDDING_DEVICE
)

# load csv file
df = pd.read_csv('questions.csv')
vecs = []

for _, row in df.iterrows():

        payload = {"query": row['domande'],
                    "role": row['ruolo'],
                    "dev": "false"}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result")


            # create vector
            vecs.append(model.encode(result))

            #print(result)
            print(f"Response to question: {row['indice']}.\n")
        else:
            print(f"Errore {response.status_code}: {response.text}")
            vecs.append(None)  # placeholder
            chatbot_erros += 1

        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break

# add lines to dataframe
model_name = args.model
valid = [v is not None for v in vecs]
df_out = df[valid].copy()
df_out[model_name] = [json.dumps(v.tolist()) for v in vecs if v is not None]
df_out.to_csv('questions.csv', index=False)

# recap
print(f"Add {len(vecs)} responses, model: {model_name}")
print(f"Chatbot errors: {chatbot_erros}")