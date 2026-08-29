'''
data_summary.py is designed to gather quantitative analytics on the overall dataset used in this final 
'''

import pandas as pd
import matplotlib.pyplot as plt

# load the data for analysis
df = pd.read_csv("data/filtered_job_skills_for_pca.csv")

# Separate numeric features
numeric_df = df.select_dtypes(include=["number"])

# using describe() lets gather stats on this filtered dataset 
desc = numeric_df.describe()
print("\n Descriptive Statistics:")
print(desc)
desc.to_csv("summary_stats.csv")

# calc means and standard dev
mean_vals = numeric_df.mean().sort_values(ascending=False)
std_vals = numeric_df.std().sort_values(ascending=False)

print("\n Mean")
print(mean_vals.head(10))

print("\n Standard Dev")
print(std_vals.head(10))

mean_vals.to_csv("mean_values.csv")
std_vals.to_csv("std_values.csv")

# calc correlation between numeric features
corr = numeric_df.corr()
corr.to_csv("correlation_matrix.csv")

'''
generate boxplot on all features
'''
plt.figure()
numeric_df.boxplot(rot=90)
plt.title("Box Plot of All Skill Features")
plt.ylabel("Scaled Value")
plt.tight_layout()
plt.savefig("boxplot_all_features.png")
plt.close()

# generate barchart of mean skill importance (skillset label) and mean value
plt.figure()
mean_vals.plot(kind='bar')
plt.title("Mean Skill Importance Across Job Roles")
plt.ylabel("Mean Value")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("barplot_skill_means.png")
plt.close()
