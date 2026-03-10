# Jacob Curtis
# 2/12/2026
# HW 4

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans, MeanShift, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.stats import gaussian_kde


'''
Read in data Spotify_Youtube.csv - Part 1 of HW 4
'''
data = pd.read_csv("data/Spotify_Youtube.csv")

# read in raw data from dataset, Liveness, Energy and Loudness
# .values allows for (n_samples, n_features) from the extracted columns in the dataset
X_raw_data = data[["Liveness", "Energy", "Loudness"]].dropna().values

# use case for StandardScaler in files for DBScan
# StandardScaler() needed for mean and std normalization

X = StandardScaler().fit_transform(X_raw_data)


'''
KMeans Scatter Plot for 3D data

for the clustering methods below, I utilized the Spotify_Youtube dataset for 3D visual 

per the homework requirements
'''

kmeans = KMeans(n_clusters=6, n_init=10, random_state=42)
labels = kmeans.fit_predict(X)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# scatter plot for KMeans
scatter = ax.scatter(data["Liveness"],data["Energy"],data["Loudness"],c=labels)

ax.set_title("KMeans Clusters at K=6")
ax.set_xlabel("Liveness")
ax.set_ylabel("Energy")
ax.set_zlabel("Loudness")

plt.show()


''' 
DBScan Scatter Plot for 3D data for min_samples = 7
'''
# instance of DBSCAN - shown in code from class example
dbscan = DBSCAN(eps=0.30, min_samples=7)
labels = dbscan.fit_predict(X) 

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# scatter plot for DBSCAN
scatter = ax.scatter(data["Liveness"],data["Energy"],data["Loudness"],c=labels)

ax.set_title("DBSCAN Clusters w/ Min Points=7")
ax.set_xlabel("Liveness")
ax.set_ylabel("Energy")
ax.set_zlabel("Loudness")

plt.show()



'''
Mean-Shift Scatter Plot for 3D data
'''
# instance of MeanShift as shown in code example from class
meanshift = MeanShift(bandwidth=1.1, bin_seeding=True)
labels = meanshift.fit_predict(X)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# scatter plot for Mean-Shift
scatter = ax.scatter(data["Liveness"],data["Energy"],data["Loudness"],c=labels)

ax.set_title("Mean-Shift Clusters w/ Radius 1.1")
ax.set_xlabel("Liveness")
ax.set_ylabel("Energy")
ax.set_zlabel("Loudness")

plt.show()


'''
KMeans elbow use case

inertia for kmeans values calculated in for loop

as k increases, inertia decreases as centroids are closer to smaller distances
'''
inertia = []
K = range(2, 14) # range for increasing clusters

'''
for loop for gathering inertia, and K for elbow graph
'''
for k in K:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X)
    inertia.append(km.inertia_)

'''
elbow graph for KMeans
'''
plt.figure()
plt.plot(K, inertia, marker="o")
plt.title("KMeans Elbow Graph")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.grid(True)
plt.show()


'''
DBscan use case for elbow method

where k is an arbitrary integer for the min_points
'''

# min_points chosen arbitrarily 
k = 7

neighbors = NearestNeighbors(n_neighbors=k).fit(X)

# calculate distances for the elbow graph via kneighbors of X
# kneighbors returns (distances, indices)
distances, indices = neighbors.kneighbors(X)

# k_distances sorts only the the distances furthest from the k-th neighbor
k_distances = np.sort(distances[:, -1])


'''
plotting of elbow graph for DBSCAN
'''
plt.figure()
plt.plot(k_distances)
plt.title("DBSCAN k-Distance Elbow Plot")
plt.xlabel("Points")
plt.ylabel("Distance")
plt.show()

'''
Mean-Shift use case for elbow

utilized MeanShift for simplicity

MeanShift() is used in the Mean_Shift file example as shown in canvas

I utilized a sample size of dataset as mean_shift plotting increased in computation time
'''

# Subsample test data for Mean_Shift
sample_size = 3000

index = np.random.choice(len(X), size=sample_size, replace=False)
X_mean_shift = X[index]

# initial bandwith values to test using np.linspace
# store number of clusters Mean-Shift determines for each bandwith
bandwidths = np.linspace(0.4, 1.6, 7)
num_clusters = []

# for loop - for each bandwith store cluster labels for unique clusters
for i in bandwidths:
    mean_shift = MeanShift(bandwidth=i)
    labels = mean_shift.fit_predict(X_mean_shift) # assign cluster labels
    num_clusters.append(len(set(labels))) # set avoids duplication of labels

'''
Elbow Graph for Mean-Shift
'''
plt.figure()
plt.plot(bandwidths, num_clusters, marker="o")
plt.title("Mean Shift Elbow Plot")
plt.xlabel("Radius")
plt.ylabel("Clusters")
plt.show()


'''
Part 2 Below 
'''


'''
Read in data form Iris dataset - Part 2 of HW 4
'''
data = pd.read_csv("data/Iris.csv")

# xy is defined as Petal Length and Petal Width
xy = data[["PetalLengthCm", "PetalWidthCm"]].dropna()

# counts for the frequency of petal length and petal width groupings via groupby
# counts here is a pandas dataframe storing such counts
counts = (xy.groupby(["PetalLengthCm", "PetalWidthCm"]).size().reset_index(name="count"))

'''
x, y and z axis for 3D chart

where x = petal length, y = petal width, z = count of duplicate entries (x,y)

counts is the groupby method for grouping duplication instances of petal length and width pairs
'''
x = counts["PetalLengthCm"].values 
y = counts["PetalWidthCm"].values
z = counts["count"].values

'''
3D density graph for Iris dataset 

x axis is PetalLengthCm, y is PetalWidthCm, and z the count of (x,y) duplication

where ax is the subplot figure
'''


x_grid = np.linspace(x.min(), x.max(), 100)
y_grid = np.linspace(y.min(), y.max(), 100)

# Create a mesh for x and y
x1, y1 = np.meshgrid(x_grid, y_grid)

# ravel() flattens 2d array defined in meshgrid
x_flat_array = x1.ravel()
y_flat_array = y1.ravel()

'''
define np array for x,y flat array from ravel()
'''
points = np.array([x_flat_array, y_flat_array])
kde = gaussian_kde([x, y]) # density values for density graph x_flat turns into x
z = kde(points)
z = z.reshape(x1.shape) # plot_surface requires 2D grid, thus reshape

# define figure and subplot of figure
fig = plt.figure(figsize=(13, 7))
ax = fig.add_subplot(111, projection='3d')

# surface is the subplot plot surface for the density graph
# this gives the cool density affect
surface = ax.plot_surface(x1, y1, z, cmap='coolwarm',edgecolor='none')

ax.set_xlabel('Petal Length')
ax.set_ylabel('Petal Width')
ax.set_zlabel('Count')
ax.set_title('Iris 3D Density Graph')

fig.colorbar(surface, shrink=0.5, aspect=5)
ax.view_init(80, 50)

plt.show()