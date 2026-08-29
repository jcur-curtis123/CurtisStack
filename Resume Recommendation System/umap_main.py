import os
import pandas as pd
import numpy as np
import pdfplumber
import plotly.io as pio
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import umap
from sklearn.preprocessing import MinMaxScaler
import re


# Open plots in browser
pio.renderers.default = "browser"


'''
clean_text will take in the resume text - pdf extraction 

lower case all characters and substitute " " with applicable a-z or 0-9

return this cleaned text for cosine sim method
'''

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def parse_resume_onet(text, feature_columns):
    features = {}

    for skill in feature_columns:
        keywords = skill.lower().split()
        count = 0
        for k in keywords:
            count += text.count(k)
        features[skill] = count

    return features
'''
pdf plumber opens the file as pdf and extracts each page and stores as str " " 
'''

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + " "
    return text


'''
read in excel file of skillsets as onet with pd pandas
'''

onet = pd.read_excel("data/Skills.xlsx")

# keep only the level values in the dataset
onet = onet[onet["Scale Name"] == "Level"]

# filter for given 30 construction related jobs
job_codes = [
    "11-9021.00","47-2031.00","47-2111.00","47-2221.00","47-2152.00",
    "47-2081.00","47-2132.00","47-4021.00","17-2051.00","17-2051.01",
    "47-2071.00","47-2073.00","47-4051.00","47-2151.00","47-2072.00",
    "47-2171.00","47-4061.00","47-1011.00","13-1082.00","11-9041.00",
    "11-3013.00","49-9021.00","47-2141.00","47-3011.00","47-2021.00",
    "47-2061.00","17-3022.00","47-4099.00","47-4011.00","47-2231.00"
]

onet = onet[onet["O*NET-SOC Code"].isin(job_codes)]

'''
Pivot into matrix:

Rows  = O*NET codes
Columns = skills (Element Name)
Values = skill level (Data Value)
'''
pivot = onet.pivot(
    index="O*NET-SOC Code",
    columns="Element Name",
    values="Data Value"
)

# SCALE DATA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(pivot)

# UMAP
umap_model = umap.UMAP(
    n_components=2,
    n_neighbors=5,
    min_dist=0.2,
    random_state=42
)

X_umap_jobs = umap_model.fit_transform(X_scaled)

# fill na with 0 integer values - useful for cosine sim 
pivot = pivot.fillna(0)


# keep only values >0.1 in value
pivot = pivot.loc[:, pivot.var() > 0.1]

# store feature columns as element name - defined previously in pivot
FEATURE_COLUMNS = pivot.columns

# job_roles is onet codes from pivot df
job_roles = pivot.index

resume_folder = "data/resumes"

for filename in os.listdir(resume_folder):

    filepath = os.path.join(resume_folder, filename)

    # similar logic to main.py for PCA, we extract skillsets from given resume
    text = extract_text_from_pdf(filepath)
    text = clean_text(text)

    # features defined upon parsing the resume, matching with onet codes
    # df resume is stored as a pd dataframe with features vector from resume and 
    # feature vector from onet skills
    features = parse_resume_onet(text, FEATURE_COLUMNS)
    df_resume = pd.DataFrame([features])[FEATURE_COLUMNS]
    X_res_scaled = scaler.transform(df_resume)
    X_res_umap = umap_model.transform(X_res_scaled)
    
    print(f"\nResume: {filename}")
    print(df_resume.head())

    # cosine similarity on res umap and umap jobs 
    # sort the cosine sim with top 3
    sim_umap = cosine_similarity(X_res_umap, X_umap_jobs).flatten()
    top_idx = sim_umap.argsort()[::-1][:3]

    print("\nTop Matches (With UMAP):")
    for i in top_idx:
        print(f" - {job_roles[i]} (score: {sim_umap[i]:.4f})")

    # visualization for UMAP implementation
    df_jobs = pd.DataFrame(X_umap_jobs, columns=["UMAP1", "UMAP2"])
    df_jobs["label"] = job_roles

    # plot the UMAP visual 
    fig = px.scatter(
    df_jobs,
    x="UMAP1",
    y="UMAP2",
    text="label",
    title="UMAP Job Space"
    )   

    fig.update_traces(textposition="top center")
    fig.show()