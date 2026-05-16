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


# Config lingotto url
BASE_URL = "http://127.0.0.1"
PORT = "5050"
ENDPOINT = "/api/response"  

# URL
url = f"{BASE_URL}:{PORT}{ENDPOINT}"

response = requests.get(url)

# error counters
wrong_role = 0 
wrong_arg = 0

last_response_time = None


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
        current_response_time = time.perf_counter()

        if last_response_time is None:
            elapsed = 0
        else:
            elapsed = current_response_time - last_response_time

        last_response_time = current_response_time

        if response.status_code == 200:
            data = response.json()
            result = data.get("result")

            #resuls cleaning
            result = result.split("Puoi consultare")[0].strip()
            result_low = result.lower()
            pattern_sezione = r"(sezione dedicata al profilo|effettua il logout|accedi nuovamente selezionando il ruolo).*(shop|backoffice|lab|commerciante)"
            pattern_rifiuto = r"(non posso rispondere|non include funzionalità|documentazione.*non include|mi dispiace|non dispongo di informazioni|non contiene informazioni specifiche|non ho informazioni sufficienti|non fornisce informazioni specifiche|non sono in grado di rispondere)"

            if re.search(pattern_sezione, result_low):
                wrong_role += 1

                with open('errors.txt', 'a') as f:
                    f.write(row["domande"] + '\n\n\n\n')
                #with open('ruolo.txt', 'a') as f:
                #    f.write(row['ruolo'] + '   ' + row["domande"] + '   ' + result)
            
            if re.search(pattern_rifiuto, result_low):
                wrong_arg += 1

                with open('errors.txt', 'a') as f:
                    f.write(row["domande"] + '\n\n\n\n')
                #with open('contesto.txt', 'a') as f:
                #    f.write(row['ruolo'] + '   ' + row["domande"] + '   ' + result)

            #with open('risposte.txt', 'a') as f:
            #    f.write(row["ruolo"] + "  " + row["domande"] + "  " + result + "\n\n\n")


            # create vector
            vecs.append(model.encode(result))  # 1D vector

            #print(result)
            print(f"Risposta domanda {row['indice']}, tempo: {elapsed:.2f}.\n\n")
        else:
            print(f"Errore {response.status_code}: {response.text}")
            vecs.append(None)  # placeholder

        try:
            time.sleep(0)
        except KeyboardInterrupt:
            break

# add lines to dataframe
model_name = args.model
valid = [v is not None for v in vecs]
df_out = df[valid].copy()
df_out[model_name] = [json.dumps(v.tolist()) for v in vecs if v is not None]
df_out.to_csv('questions.csv', index=False)

# recap
print(f"Risposte fuori ruolo: {wrong_role}, risposte fuori argomento: {wrong_arg}.")