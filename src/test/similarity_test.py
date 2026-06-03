"""
SIMILARITY_TEST.PY - Statistical Evaluation & Cross-Model Cosine Similarity Analysis

This script handles the final evaluation phase of the benchmark. It reads the computed 
response embeddings from the dataset and calculates the Cosine Similarity between 
the answers of two different models to quantitatively measure their divergence.
"""


from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import json
from numpy.linalg import norm
# --------------------
# parser configuration
# --------------------
parser = argparse.ArgumentParser()
parser.add_argument("--first-model", type=str, required=True, help="First model to test")
parser.add_argument("--second-model", type=str, required=True, help="Second model to test")
parser.add_argument("--file-name", type=str, help="dataset file name, default: questions", default='questions')
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


# -----------------------
#   VECTORS EXTRACTION
# -----------------------

# first model vectors extraction
df = pd.read_csv(file_path)
v1 = np.array(df[args.first_model].apply(json.loads).tolist())

# second model vectors extraction
df = pd.read_csv(file_path)
v2 = np.array(df[args.second_model].apply(json.loads).tolist())


cosine = np.sum(v1 * v2, axis=1) / (norm(v1, axis=1) * norm(v2, axis=1))
# print("Cosine Similarity:", cosine)

print("Mean:", cosine.mean())