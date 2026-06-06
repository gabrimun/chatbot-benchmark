# Chatbot Benchmarking & Evaluation Framework

An automated testing framework designed to benchmark responses from a chatbot.
This repository covers the entire evaluation pipeline: from consolidating documentation files and generating synthetic questions, to collecting chatbot responses and calculating the statistical similarity between different LLM models.

>**Integration Assumptions**
> This framework is designed for chatbots that expose an HTTP API endpoint.
> By default, it sends HTTP POST requests with a predefined payload structure (e.g., `query`, `role`) and expects a response containing a `result` field.
>
> The current implementation reflects a role-based chatbot architecture and is **not fully plug-and-play**.
> If your chatbot differs, you will need to adapt:
>
> * the request payload (`get_response.py`)
> * the response parsing logic
> * the role-based handling (if not applicable)
>
> With these adjustments, the framework can be used with any chatbot supporting HTTP-based interaction.

---

## Test Pipeline

### 1. Build the Question Dataset (`csv_questions_builder.py`)
* **Consolidation & Cleaning:** This script aggregates documentation from multiple separate Markdown files and strips out hyperlinks, media tags, and formatting clutter. It implements a multi-role logic mapped directly from your documentation's file-system structure.
* **LLM Generation:** It injects the cleaned documentation into the target system prompt and sends it to the OpenAI API to generate a pool of synthetic user questions.
* **Output:** The generated questions are written into a structured CSV dataset. Each row contains: a unique `question_id`, the assigned `user_role` (if implemented in your chatbot architecture), and the raw `question_text`.

### 2. Collect Chatbot Responses & Embeddings (`get_response.py`)
* **Execution:** This script reads the CSV dataset and forwards each question to your chatbot endpoint via HTTP POST requests. 
* **Vector Generation:** It captures the chatbot's text response, calculates its vector embedding locally, and saves it back into the CSV dataset.
* *Note: This step must be executed at least twice using different LLM configurations/models on your chatbot to enable a cross-model comparison.*

### 3. Compute Cross-Model Cosine Similarity (`similarity_test.py`)
* **Evaluation:** This final script parses the embedding vectors from the dataset. It calculates the **Cosine Similarity** for each pair of responses generated for the exact same question.
* **Aggregation:** It stores the similarity scores in a vector and computes the global mean score, providing a quantitative metric of how much the two models diverge.


## Settings before usage

### 1. Start a virtual environment and install dependencies
* Create a venv with `python3 -m venv .venv` and activate with `source .venv/bin/activate`.
* Run `pip install -r requirements.txt` for installing all dependencies.

### 2. .env
* Copy `.env` file: `cp .env.example .env`.
* Set all variables in the `.env` file.

### 3. Documentation structure
* Ensure your local documentation folder layout strictly matches the hierarchical logic expected by `csv_questions_builder.py` (e.g., role-specific subfolders).

### 4. Payload to the chatbot
* Set the HTTP request payload in `get_response.py` to match your chatbot API implementation.


## Usage

### 1. Build the question dataset

* Run `python csv_questions_builder.py` to build the question dataset, saved in `questions.csv`.
* Optionally: `python csv_questions_builder.py --file-name my_dataset --force`
* *Note: each run will overwrite the dataset file if `--force` is used.*

**CLI Arguments**

| Argument      | Type   | Required | Default     | Description                                                                |
| ------------- | ------ | -------- | ----------- | -------------------------------------------------------------------------- |
| `--file-name` | string | No       | `questions` | Name of the output CSV file. Automatically appends `.csv` if not provided. |
| `--force`     | flag   | No       | `False`     | Overwrites the output file if it already exists.                           |

---

### 2. Get responses from the LLM model

* Run `python get_response.py --model gemini-3.1-flash-lite`
* Optionally: `python get_response.py --model gpt-4o --file-name my_dataset --force`
* This will create a new column for each model used.
* *Note: run this step multiple times with different models for comparison.*

**CLI Arguments**

| Argument      | Type   | Required | Default     | Description                                                                              |
| ------------- | ------ | -------- | ----------- | ---------------------------------------------------------------------------------------- |
| `--model`     | string | Yes      | —           | Name of the LLM model used to label the generated responses column.                      |
| `--file-name` | string | No       | `questions` | Name of the input/output CSV dataset file. Automatically appends `.csv` if not provided. |
| `--force`     | flag   | No       | `False`     | Overwrites existing model responses in the dataset if already present.                   |

---

### 3. Similarity test

* Run `python similarity_test.py --judge-model gemini-3.1-flash-lite`
* Optionally: `python similarity_test.py --judge-model gpt-4o --file-name my_dataset`
* The script compares the selected model against all other models present in the dataset.

**CLI Arguments**

| Argument        | Type   | Required | Default     | Description                                                                       |
| --------------- | ------ | -------- | ----------- | --------------------------------------------------------------------------------- |
| `--judge-model` | string | Yes      | —           | Name of the reference model used to compare embeddings against other models.      |
| `--file-name`   | string | No       | `questions` | Name of the input CSV dataset file. Automatically appends `.csv` if not provided. |
