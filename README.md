# Chatbot Benchmarking & Evaluation Framework

An automated testing framework designed to benchmark responses from a chatbot. 
This repository covers the entire evaluation pipeline: from consolidating documentation files and generating synthetic questions, to collecting chatbot responses and calculating the statistical similarity between two different LLM models.

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
* Run `python3 csv_questions_builder.py` for build the question dataset, saved in `questions.csv`.
* *Note: eanch run will rewrite the dataset file, so you will lose previous questions.*

### 2. Get responses from the LLM model
* Run `python3 get_response.py --model gemini-3.1-flash-lite` where `--model` is the LLM you are using in the chatbot, this will create a new column for each model used.
* *Note: This step must be executed at least twice using different LLM configurations/models on your chatbot to enable a cross-model comparison.*

### 3. Similarity test
* Run `python3 similarity_test.py --first_model gemini-3.1-flash-lite --second_model gpt-4o` for testing **cosine_similarity** between the two models.