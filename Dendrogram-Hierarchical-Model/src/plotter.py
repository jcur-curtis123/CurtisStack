import os
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram


class Plotter:

    def plot(self, Z, labels, save_dir="figures"):

        '''
        let's give each plot a name, so we can save properly in plt.savefig

        I've used scipy's dendrogram - a function in the Scipy 

        Python's dendrogram requires Z or the linkage matrix, and county labels
        '''
        filename = f"dendrogram.png"
        filepath = os.path.join(save_dir, filename)

        
        plt.figure(figsize=(12, 6))
        # see https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html
        dendrogram(Z, labels=labels, leaf_rotation=90)
        plt.tight_layout()

        '''
        Inspiration from the pandas assignment - I've decided to save figures for presentation purposes.

        Figures are saved to figures directory
        '''
        plt.savefig(filepath, dpi=300) # save figure with filepath

        # allow for plot to show - from pandas practice
        plt.show()
