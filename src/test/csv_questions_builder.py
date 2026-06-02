"""
CSV_QUESTIONS_BUILDER.PY - Automated Dataset Generator (Synthetic Testing Questions)

This script scans the software documentation organized by user-role folders,
cleans the Markdown files by removing non-textual elements (links, images, tables),
and leverages an LLM (OpenAI) to generate a set of synthetic user questions for each role.

ROLE-DEPENDENCY WARNING:
This script tightly relies on a directory structure based on user roles (i.e., the PATH 
environment variable must point to a directory containing subfolders like 'shop', 'backoffice', etc.).

If the chatbot or software under test DOES NOT implement a role-based logic:
1. Remove the outer loop: `for role in sorted(path.iterdir()):`.
2. Modify the Markdown file collection (`role.rglob("*.md")`) to directly scan a single, 
   centralized folder containing the global documentation.
3. In both the LLM system prompt and the DataFrame creation, remove any references 
   to the role context (e.g., fallback the 'ruolo' field to a fixed value like 'generic').
"""


from pathlib import Path
from prompt import *
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
import pandas as pd
from pandas.errors import EmptyDataError

load_dotenv()

path = Path(os.getenv("DATA_PATH"))

# new dataframe
df = pd.DataFrame(columns=['index', 'role', 'question'])

rows = []
# index counter
indice_counter = 1

#------------------------------------------------------
# Generating unified documentation from multiple files
#------------------------------------------------------

for role in sorted(path.iterdir()):
    # filesystem tree iteration
    print(f"Creazione documentazione per {role.name}...") 
    file_name = role.name + '.txt'
    
    documentation = ""
    for file in sorted(role.rglob("*.md")):

        if file.name != '00-index.md':
            with open(file, "r", encoding="utf-8") as f:
                md_content = f.read()

                md_no_link = re.sub(r'!\[.*?\]\(.*?\)', '', md_content) # remove images link
                md_no_link = re.sub(r'\[.*?\]\(.*?\)', '', md_no_link)  # remove navigation links
                md_no_link = re.sub(r'\s*\|\s*', ' ', md_no_link)

                documentation = documentation + md_no_link + "\n\n\n\n"
            
    print(f"... terminata composizione documentazione per {role.name}")

    # send questions request to OpenAI api 
    print(f"Inizio scrittura domande per {role.name}...")
    prompt = PROMPT + documentation

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
    print(f"... fine scrittura domande.")


# add lines to dataframe
if rows:
    new_df = pd.DataFrame(rows)
    df = pd.concat([df, new_df], ignore_index=True)

# add index column
print("Aggiungo le domande al dataframe...")
df = df[['indice', 'ruolo', 'domande']]
df.to_csv('questions.csv', index=False)
print("... aggiunta domande terminata")
