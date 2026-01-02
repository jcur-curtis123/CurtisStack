# Introduction
The goal for this project is to identify counties that are close in similarity given data regarding Fair Market Rent and Income metrics. Identifying counties with low FMR or high FMR may explain housing affordability at a county comparison approach. 

This approach utilizes concepts of unsupervised machine learning - specifically that of hierarchical clustering. 

In essence, I attempt to answer the question, "Where are renters most cost-burdened relative to local incomes, and with this, how do regional housing markets cluster by affordability conditions?"

Also, in what ways can decision makers view and propose changes on high FMR counties with respect to that of low FMR counties, given the output of the hierarchical clustering algorithm - the dendrogram. 

Please see the work cited portion of this README for data sources. 

Please run requirements.txt via 

pip install -r requirements.txt

This .txt file includes:

pandas,
numpy,
matplotlib,
scipy

This is required in order for main.py to compile correctly. 

*Note* If pip does not work, try pip3 install -r requirements.txt.

You may see your version of pip via pip3 -v. 

# Object Oriented Method

The object oriented method utilized for this project is that of the factory method. The factory method is a method listed on the refactoring.guru site. This method made the most sense to work with as I have separate components of information within my overall project. Each component acts as a dataloader, and the factory method will "load" each dataloader.

Let's take a look at each step of the factory method:

In the main.py, the driver for this project, a Pipeline instance is created with the FMR, Wage, and Income csv files. Pipeline.main() is called, and within main(), objects for Dataloader and LoaderFactory are created. Dataloader assigns counties from the listed csvs as CountyData objects. Each CountyData object has a self.fmr, self.wage, and self.income attribute, these are also features for each county.

The LoaderFactory manages which loader class is created given a string. The "factory" essentially manufactures loader classes to be used in DataLoader and CountyData. 

From here, model.py builds the matrix (fmr, wage, and household income) and also normalizes this county data. After normalization and construction of the matrix, cluster() returns Z matrix for the dendrogram.

Plotter.py includes the logic for plotting the dendrogram.

Pipeline takes the model and logic from plotter and plots the dendrogram given the prior steps of establishing a matrix level format of the csv data.

A diagram representing how this Factory Method works is located in docs/DS_5010_Final.png

# Data Preparation 

As mentioned prior, the individual loaders "load" each csv accordingly. Below is an example of how the loader will load the csv. 

```python
def load(self, path, store):
    with open(path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            county = store.get(row["County"])
            county.fmr = float(row["FMR_2BR"])
```

An example of get() from dataloader.py

```python
def get(self, name):

        clean = name.replace(" County", "").strip()
        if clean not in self.counties:
            self.counties[clean] = CountyData(clean)
        return self.counties[clean]
```

County is stored as a CountyData object and it's self.fmr is set to FMR_2BR, where FMR_2BR is a standard in affordability analysis. 

Each loader is formatted this way, where each row is read and cleaned with it's corresponding csv in config.py, where paths for each csv exist.

During the development of this project, I understood that I would need to standardize or normalize the dataset during matrix construction and the development of features. Much of feature matrices were that of the numerical portions of the county data, as mentioned prior. 

For example, the FMR, Average Weekly Income, and Median Household Income is among the numerical features required. 

The formula: (X-Mean)/sigma is an approach at standardizing each X value in the feature matrix.

# Cluster Analysis

*Note - Cluster() has been refactored for calculation of Z matrix. Linkage is not utilized.*

Given a feature matrix X, Cluster() computes the initial pairwise distance matrix.

Cluster() extracts from the feature matrix and creates the Z (n-1 x 4) matrix. Z holds the information needed for the creation of the dendrogram. The Z matrix is composed of cluster ID with the pairwise distance, and its size of merging the two clusters.

This is a very important part of this project, as we must differentiate which clusters are "closests" to one another. Thus, this may answer the question as to which counties need the most attention for housing and affordability. 

The distance formula: 

$$
D_{\text{avg}}(A,B)
= \frac{1}{|A|\cdot|B|}
\sum_{p \in A} \sum_{q \in B} D(p,q)
$$

Using this distance formula, each pairwise distance is calculated for each cluster within A and B. 

A representation of the distance calculation is:

Cluster A: \(A = \{x_1, x_2\}\)
Cluster B: \(B = \{x_3\}\)

Normalized data points:

| Point | Vector      |
|-------|-------------|
| \(x_1\) | (1.0, 2.0) |
| \(x_2\) | (2.0, 3.0) |
| \(x_3\) | (0.0, 1.0) |

---

We compute the Euclidean distance \(D(p,q)\) for all  
\(p \in A\), \(q \in B\).

**Distance 1: \(D(x_1, x_3)\)**

$$
D(x_1, x_3)
= \sqrt{(1-0)^2 + (2-1)^2}
= \sqrt{1 + 1}
= \sqrt{2}
\approx 1.414
$$

**Distance 2: \(D(x_2, x_3)\)**

$$
D(x_2, x_3)
= \sqrt{(2-0)^2 + (3-1)^2}
= \sqrt{4 + 4}
= \sqrt{8}
\approx 2.828
$$

Now we must compute the average distance using Linkage Average Pariwise Distance Formula


Cluster sizes: \(|A| = 2\), \(|B| = 1\)

The average linkage formula:

$$
D_{\text{avg}}(A,B)
= \frac{1}{|A| \cdot |B|}
  \sum_{p \in A} \sum_{q \in B} D(p,q)
$$

Plug in the distances:

$$
D_{\text{avg}}(A,B)
= \frac{1}{2 \cdot 1}
  \left(1.414 + 2.828\right)
$$

$$
D_{\text{avg}}(A,B)
= \frac{4.242}{2}
= 2.121
$$

The average linkage distance between clusters A and B is:

$$
{D_{\text{avg}}(A,B) = 2.121}
$$

# Results

The overall results from running the model is an output of the dendrogram. Each county is clustered based on similarity. The similarity is determined in the pipeline via model.py's cluster() function. 

Therefore counties that have the shortest distance, will result in a merge. You will see in this instance, Penobscot and Androscoggin county are clustered together, demonstrating a similarity given the proposed datasets. 

Outliers in this dendrogram are separated from other clusters. Also, outliers may exist as a singleton, a cluster by itself. Cumberland and York counties are considered outliers. 

Why? These counties have the highest median household income, the highest average weekly net income, and FMR2BR is also the highest in these two counties. 

Counties like that of Washington and Aroostook are merged as these counties have the lowest income and FMR. 

One question that arises during the implementation of the dendrogram is, "what counties are highest in relative fmr but with comparative low income?" 

Knox County is the county that satisfies this question. With relative high fmr, it's average weekly wage is that of penobscot county, at 1,150.

The results collected from the dendrogram prompts further questioning on how the State of Maine resovles housing affordability. This project primarily focuses on renters with FMR detailing the rent per month. 

With this being said, if one municipality changes or alters legislation in their county, will this affect the county that has the lowest neighboring distance? In other words, will changes in Penobscot alter that of Knox, or even further in that of Hancock or Lincoln?

What other direct or indirect changes will affect neighboring counties considering their prospective pairwise distances? 

# Reflection

This project considered my passion for housing affordability and served as a testament to my data science skills. 

This is the first time blending a variety of python packages including, numpy, scipy, matplotlib and pandas in a singular project. 

If I were to complete this project over again, I would start with an end in mind. When it comes to building this dendrogram, I was consistently adding more datasets to see if the clusters would change or shift. This became time consuming, and I am unsure if this method of discovery is worth utilizing an extended number of resources. 

 I would also consider population, and distance to nearest neccessary services. This includes hospitals, grocery stores, and municipal buildings. These factors may contribute to a low or high population in a given county, thus, affecting the affordabiltiy in the given county. 

# Work Cited

Median Household Income by County

https://hdpulse.nimhd.nih.gov/data-portal/social/table?age=001&age_options=ageall_1&demo=00010&demo_options=income_3&race=00&race_options=race_7&sex=0&sex_options=sexboth_1&socialtopic=030&socialtopic_options=social_6&statefips=23&statefips_options=area_states

Average Weekly Wage

https://www.bls.gov/regions/northeast/news-release/2025/countyemploymentandwages_maine_20250612.htm#QCEWMETable2.xlsx.f.1

FMR - Maine

https://www.mainehousing.org/docs/default-source/asset-management/rent-income-charts/2024-rent-income-charts.pdf?sfvrsn=f5ea9e15_2

Factory Method

https://refactoring.guru/design-patterns/factory-method

Population Data

https://worldpopulationreview.com/us-counties/maine 

LLMs Used:

During the discovery phase of this final, I utilized Claude for assistance on understanding Dendrograms. I spent ~8 hours on researching and watching content related to unsupervised machine learning and the use of dendrograms. An example of content watched was this youtube video: https://www.youtube.com/watch?v=IUn8k5zSI6g, Crash Course Statistics' video on Dendrograms. This process assisted with my understanding with unsupervised machine learning, a great bridge into Unsupervised Machine Learning course. 

Research also included that of the Factory Method. After gathering information from refactoring.guru, I clarified that factory method is indeed an OOP concept as well as, clarification on if such concept can work alongside the Hierarchical Clustering within Unsupervised Machine Learning.

Overall, I was able to successfully understand the factory method and it's approach with Object Oriented Programming (OOP). 
