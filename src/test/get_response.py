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
from pathlib import Path
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
parser.add_argument("--file-name", type=str, help="dataset file name, default: questions", default='questions')
parser.add_argument("--force", help="Overwrite the existing dataset file if it already exists.", action='store_true')

args = parser.parse_args()

f_name = args.file_name if args.file_name.endswith('.csv') else args.file_name + '.csv'

# dataset directory setup
project_root = Path(__file__).resolve().parent.parent.parent
dataset_dir = project_root / 'dataset'

# csv file path
file_path = dataset_dir / f_name

if not file_path.is_file():
    print(f"Dataset '{f_name}' doesn't exist.")
    exit()

# load csv file
df = pd.read_csv(file_path)
vecs = []

if args.model in df.columns and not args.force:
    print(f"Responses for model {args.model} already exists. Change the model or use the --force argument to overwrite it.")
    exit()

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
df_out.to_csv(file_path, index=False)

# recap
print(f"Add {len(vecs)} responses, model: {model_name}")
print(f"Chatbot errors: {chatbot_erros}")