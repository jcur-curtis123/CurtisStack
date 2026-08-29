import os
import re
import numpy as np
import pandas as pd
import pdfplumber
import plotly.express as px
import plotly.io as pio

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

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


pivot_reset = pivot.reset_index()

# Save to CSV
pivot_reset.to_csv("data/filtered_job_skills_for_pca.csv", index=False)

# fill na with 0 integer values - useful for cosine sim 
pivot = pivot.fillna(0)


# keep only values >0.1 in value
pivot = pivot.loc[:, pivot.var() > 0.1]

# store feature columns as element name - defined previously in pivot
FEATURE_COLUMNS = pivot.columns

# job_roles is onet codes from pivot df
job_roles = pivot.index

# scale df with min_max scale
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(pivot)


'''
this section of the program is the defining of PCA, we will decide to have 3 pca components
'''
pca = PCA(n_components=3)

# utilize scaled df pivot for pca fit transform
# fit_transform computes the dimensionality reduction on X_scaled
X_pca_jobs = pca.fit_transform(X_scaled)

print("\nExplained Variance (PCA):", pca.explained_variance_ratio_)


'''
We derive keywords directly from skill names instead of
manually defining categories.

This allows for any n columns for any skillset ONET dataset - future scalability opportunity
'''


# generate_keywords will take in feature columns 
# and will generate words used 
def generate_keywords(skill_name):
    words = skill_name.lower().split()
    return words

# ONET keywords is a dictionary 
# and will return {"Mechanical: [mechanical]"}
ONET_KEYWORDS = {
    skill: generate_keywords(skill)
    for skill in FEATURE_COLUMNS
}

'''
parse resume onet skillsets, this will read pdf resume 

and match based on skills in resume and onet skillset dictionary 
'''

def parse_resume_onet(text):
    text = clean_text(text)
    return {
        skill: sum(len(re.findall(word, text)) for word in keywords)
        for skill, keywords in ONET_KEYWORDS.items()
    }


resume_folder = "data/resumes"

'''
for loop for extracting text from resumes
'''

for filename in os.listdir(resume_folder):
    filepath = os.path.join(resume_folder, filename)

    print("\n----")
    print(f"Resume: {filename}")

    # Load resume text
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(filepath)
    else:
        with open(filepath, "r") as f:
            text = f.read()

    '''
    Extract O*NET skill features from resume
    '''
    features = parse_resume_onet(text)
    df_resume = pd.DataFrame([features])[FEATURE_COLUMNS].fillna(0)
    print(df_resume)

    '''
    Scale resume features using same scaler
    '''
    X_res_scaled = scaler.transform(df_resume)

   # compute cosine similarity pre pca transformation
    sim_raw = cosine_similarity(X_res_scaled, X_scaled)[0]
    top_idx_raw = sim_raw.argsort()[-3:][::-1]

    print("\nTop Matches without PCA:")
    for i in top_idx_raw:
        print(f" - {job_roles[i]} (score: {sim_raw[i]:.4f})")

    # compute the pca transform on min max scaled resume data
    # pca sim is the similarity score on the pca transformed data - post dimensionality reduction 
    X_res_pca = pca.transform(X_res_scaled)
    sim_pca = cosine_similarity(X_res_pca, X_pca_jobs)[0]
    top_idx_pca = sim_pca.argsort()[-3:][::-1]

    print("\nTop Matches (WITH PCA):")
    for i in top_idx_pca:
        print(f" - {job_roles[i]} (score: {sim_pca[i]:.4f})")

    
    '''
    let's store pca jobs as a pd dataframe and the applicable columns named accordingly on pca #

    resume will also be stored as pd df, thus allowing the resume to 'live' in this space for 3d visual
    '''
    df_jobs_pca = pd.DataFrame(X_pca_jobs, columns=['PC1', 'PC2', 'PC3'])
    df_jobs_pca['type'] = 'Job'
    df_jobs_pca['label'] = job_roles

    # Resume loaded into PCA 3D 
    df_res_pca = pd.DataFrame(X_res_pca, columns=['PC1', 'PC2', 'PC3'])
    df_res_pca['type'] = 'Resume'
    df_res_pca['label'] = filename

    df_all = pd.concat([df_jobs_pca, df_res_pca], ignore_index=True)

    df_all['size'] = df_all['type'].map({
        'Job': 4,
        'Resume': 14
    })

    '''
    3D PCA visual using px scatter
    '''
    fig = px.scatter_3d(
        df_all,
        x='PC1',
        y='PC2',
        z='PC3',
        color='type',
        size='size',
        hover_name='label',
        title=f"3D PCA: Resume vs Job Space ({filename})"
    )

    fig.update_layout(
        scene=dict(
            xaxis_title='PC1',
            yaxis_title='PC2',
            zaxis_title='PC3'
        )
    )

    fig.show()