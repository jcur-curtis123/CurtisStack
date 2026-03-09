import numpy as np


class Model:

    '''
    Model holds the technique for building model matrix
    
    and normalizing the matrix for proper clustering
    '''

    def build_matrix(self, counties):

        '''
        build_matrix is the project's sole way of building a feature matrix for distance calculations

        X includes FMR, Wage, and Income data for each county

        Labels are the county name and X is the feature matrix - both are returned in cluster

        '''
        
        X = []
        labels = []
        for county in counties:
            X.append(county.compute_features())
            labels.append(county.name)

        return np.array(X), labels

    def normalize(self, X):

        '''
        In order to run cluster analysis on the county data, I need to normalize features

        This disallows for higher distances to dominate the average cluster ward distance
        '''

        mean = X.mean(axis=0)
        sigma = X.std(axis=0)


        return (X - mean) / sigma # return normalized score for each county


    def cluster(self, X_norm):

        '''
        cluster() creates the Z matrix required for Dendrogram plot

        Within this function, cluster assigns ID's to each cluster - where cluster is normalized in X vector

        Z matrix is initialized and new cluster IDs are appended 

        Average distance between the 2 clusters (at a given instance) is also appended to Z

        Redefined cluster IDs, AVG best distances, and cluster size are all utilized for Z

        '''
        
        n = len(X_norm)

        # clusters will contain the number of n counties
        clusters = []
        for i in range(len(X_norm)):
            clusters.append([i])  
      

        cluster_ids = list(range(n))

        Z = []       
        next_id = len(X_norm)   

    
        while len(clusters) > 1:

            best_dist = float("inf")
            best_i = None
            best_j = None

            '''
            nested for loop for computing euclidean distances between clusters

            assign A and B as comparing 2 clusters at once

            their distance will be stored in dists

            '''
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):

                    A = clusters[i]
                    B = clusters[j]

                    dists = []

                    '''
                    for values in A let's calculate the distance of each vector

                    with np's linalg - we can calculate the euclidean distance

                    these values are now part of the dists list containing all distances form A and B

                    '''

                    for p in A:
                        for q in B:
                            diff = X_norm[p] - X_norm[q]
                            d = np.linalg.norm(diff)
                            dists.append(d)
                    
                    # calculate the average dist
                    avg_dist = sum(dists) / len(dists)

                    '''
                    if current avg_dist less than the best_dist then...

                    best_dist is the avg_dist and the loop continues until termination

                    we gather best_dist, best_i and best_j
                    '''
                    if avg_dist < best_dist:
                        best_dist = avg_dist
                        best_i = i
                        best_j = j

            # define clusters A and B - local best cluster
            A = clusters[best_i]
            B = clusters[best_j]

            # merge these two clusters
            merged = A + B
            merged_size = len(merged)

            # cluster ID for A and B are defined 
            # without cluster ID idA, and idB, cluster index would be used
            # clusters after merging are appended, thus changing place in list
            idA = cluster_ids[best_i]
            idB = cluster_ids[best_j]

            '''
            This is our Z matrix, required for Dendrogram

            This Z matrix contains Id of each cluster, the best distance, and cluster merged size
            '''
            Z.append([min(idA, idB), max(idA, idB), best_dist, merged_size])

            '''
            after each iteration, clusters that are already merged

            remove from clusters list, this will avoid duplicate merge of clusters
            '''
            clusters.pop(best_j)
            cluster_ids.pop(best_j)

            clusters.pop(best_i)
            cluster_ids.pop(best_i)

            '''
            merged clusters will serve as indexed in clusters

            ie; clusters = [[0], [1], [2,3]]

            clusters are reassigned ids for Scipy's dendrogram

            this is the idA, idB format shown in Z matrix
            '''
            clusters.append(merged)
            cluster_ids.append(next_id)
            next_id += 1
        
        # np array required for dendrogram in plotter.py
        return np.array(Z)