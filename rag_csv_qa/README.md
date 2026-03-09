---
title: "Local AI Analytics with RAG (Government Spending)"
author: "Jacob Curtis"
output: github_document
---

## Overview

This project implements a local Retrieval-Augmented Generation (RAG) system that enables natural-language analysis of U.S. government spending data stored in CSV format.

The system uses vector similarity search to retrieve relevant rows and a locally hosted LLM to generate answers. 

Example questions:

- *What are the long-term trends in federal outlays?*
- *How has the federal deficit changed over time?*
- *Are there years with unusually large spending increases?*

---

## Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3 |
| Data Processing | Pandas |
| Embeddings | Ollama (`nomic-embed-text`) |
| Vector Store | FAISS |
| Language Model | Ollama (`llama3.1:8b`) |
| RAG Utilities | LangChain (core + community) |
| Execution | Local CLI |

---

## Dataset

This project uses **public U.S. federal budget data** provided as a CSV file.

### Download dataset

curl -L -o gov_spending.csv \
https://raw.githubusercontent.com/datasets/federal-budget/master/data/federal-budget.csv

### Rename to match config

mv gov_spending.csv data.csv

### Environment Setup

Create a Python VM:

python3 -m venv myenv

Activate: 

source myenv/bin/activate

Required dependencies are:

pip install pandas langchain langchain-core langchain-community faiss-cpu

### Ollama Setup

ollama pull llama3.1:8b
ollama pull nomic-embed-text

### License 

License
Public datasets are used under their respective open licenses.
This project is provided for educational and demonstration purposes.