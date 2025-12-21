# Introduction

To install the proper prerequisites: 

For macOS or Linux:
- A C++ compiler (`clang++` or `g++`)
- SQLite3 and SQLite development headers

---

### 1. Install a C++ Compiler


xcode-select --install

### 2. Install SQLite


brew install sqlite


### Each file must be compiled. Therefore, from the project directory:

clang++ \
src/main.cpp \
src/db/Database.cpp \
src/ingest/CsvReader.cpp \
src/ingest/HousingIngest.cpp \
src/ml/StandardScaler.cpp \
src/ml/KMeans.cpp \
src/ml/PCA.cpp \
-o app \
-lsqlite3

### You may run the application via:

./app

### To open the SQLite database:

sqlite3 housing.db

---

## Housing Market Segmentation with C++, SQLite, and Unsupervised Learning

This project implements an end-to-end unsupervised machine learning pipeline in C++, using a real housing dataset, SQLite for management of the dataset, and custom implementations of feature scaling, K-Means clustering, and PCA.

Unlike typical ML projects that rely on Python libraries, all core data engineering and machine learning logic here is written from scratch in C++, thus, demonstrating systems-level understanding of both data pipelines and ML algorithms.

---

## Project Overview

The goal of this project is to discover natural structure in housing data without using labeled outcomes.

Specifically, the system:
- Loads raw housing data from CSV
- Stores and manages it in SQLite
- Transforms features into a numeric matrix
- Applies standardization
- Performs K-Means clustering
- Applies Principal Component Analysis (PCA)

This mirrors how real production analytics systems are built.

---

## Dataset

- Source: Kaggle Housing Dataset (`Housing.csv`)
- Rows: 545 houses
- Features (13 total):
  - Price
  - Area
  - Bedrooms
  - Bathrooms
  - Stories
  - Parking
  - Main road access
  - Guest room
  - Basement
  - Hot water heating
  - Air conditioning
  - Preferred area
  - Furnishing status

