"""
SIMILARITY_TEST.PY - Statistical Evaluation & Cross-Model Cosine Similarity Analysis

This script handles the final evaluation phase of the benchmark. It reads the computed 
response embeddings from the dataset and calculates the Cosine Similarity between 
the answers of two different models to quantitatively measure their divergence.
"""

import argparse
import pandas as pd
import numpy as np
import json
from numpy.linalg import norm
# --------------------
# parser configuration
# --------------------
parser = argparse.ArgumentParser()
parser.add_argument("--first_model", type=str, required=True, help="First model to test")
parser.add_argument("--second_model", type=str, required=True, help="Second model to test")
args = parser.parse_args()


# -----------------------
#   VECTORS EXTRACTION
# -----------------------

# first model vectors extraction
df = pd.read_csv('questions.csv')
v1 = np.array(df[args.first_model].apply(json.loads).tolist())

# second model vectors extraction
df = pd.read_csv('questions.csv')
v2 = np.array(df[args.second_model].apply(json.loads).tolist())


cosine = np.sum(v1 * v2, axis=1) / (norm(v1, axis=1) * norm(v2, axis=1))
# print("Cosine Similarity:", cosine)

print("Mean:", cosine.mean())