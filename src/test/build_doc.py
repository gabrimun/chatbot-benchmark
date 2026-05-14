from pathlib import Path
from prompt import *
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
import pandas as pd
from pandas.errors import EmptyDataError

load_dotenv()

path = Path('/home/gab/Scrivania/tirocinio/test-lingotto/user')


try:
    df = pd.read_csv('prova.csv')
except EmptyDataError:
    df = pd.DataFrame(columns=['indice', 'ruolo', 'domande'])

rows = []
# index counter
indice_counter = len(df) + 1

for role in sorted(path.iterdir()):
    # iterazione sottocartelle di user
    print(f"Creazione documentazione per {role.name}...") 
    documentation = ""
    for file in sorted(role.rglob("*.md")):

        if file.name != '00-index.md':
            with open(file, "r", encoding="utf-8") as f:
                md_content = f.read()

                md_no_link = re.sub(r'!\[.*?\]\(.*?\)', '', md_content) # remove images link
                md_no_link = re.sub(r'\[.*?\]\(.*?\)', '', md_no_link)    # remove navigation links
                md_no_link = re.sub(r'\s*\|\s*', ' ', md_no_link)

                documentation = documentation + md_no_link + "\n\n\n\n"
            
                #print(documentation)
    print(f"... terminata composizione documentazione per {role.name}")

    # invio richiesta per creazione domande
    print(f"Inizio scrittura domande per {role.name}...")
    prompt = PROMPT + documentation

    #api_key = os.getenv("API_KEY") 
    #base_url = os.getenv("BASE_URL")

    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"))

    response = client.chat.completions.create(
        model= os.getenv("MODEL"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Crea delle domande che un dipendente che utilizza questo software potrebbe fare"}
        ]
    )
    questions = response.choices[0].message.content or ""

    line_questions = questions.splitlines()

    for question in line_questions:
        rows.append({'indice': indice_counter, 'ruolo': role.name, 'domande': question})
        indice_counter += 1
    

    #with open('questions.md', 'a') as f:
    #    f.write(f"{role.name}\n")
    #    f.write(f"{questions} \n\n\n")

    print(f"... fine scrittura domande.")

# add lines to dataframe
if rows:
    new_df = pd.DataFrame(rows)
    df = pd.concat([df, new_df], ignore_index=True)

# add index column
print("Aggiungo le domande al dataframe...")
df = df[['indice', 'ruolo', 'domande']]
df.to_csv('prova.csv', index=False)
print("... aggiunta domande terminata")
