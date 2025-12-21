#include "KMeans.h"
#include <cmath>
#include <cstdlib>

KMeans::KMeans(int k, int max_iters)
    : k_(k), max_iters_(max_iters) {}

double KMeans::distance(const std::vector<double>& a,
                        const std::vector<double>& b) {
    double sum = 0.0;
    for (size_t i = 0; i < a.size(); i++) {
        double diff = a[i] - b[i];
        sum += diff * diff;
    }
    return std::sqrt(sum);
}

void KMeans::fit(const std::vector<std::vector<double>>& data) {
    int n = data.size();
    int d = data[0].size();

    labels_.assign(n, 0);
    centroids_.assign(k_, std::vector<double>(d, 0.0));

    // --- 1️⃣ Initialize centroids (first k points)
    for (int i = 0; i < k_; i++) {
        centroids_[i] = data[i];
    }

    for (int iter = 0; iter < max_iters_; iter++) {
        bool changed = false;

        // --- 2️⃣ Assignment step
        for (int i = 0; i < n; i++) {
            double best_dist = distance(data[i], centroids_[0]);
            int best_cluster = 0;

            for (int c = 1; c < k_; c++) {
                double dist = distance(data[i], centroids_[c]);
                if (dist < best_dist) {
                    best_dist = dist;
                    best_cluster = c;
                }
            }

            if (labels_[i] != best_cluster) {
                labels_[i] = best_cluster;
                changed = true;
            }
        }

        // Stop if no changes
        if (!changed) break;

        // --- 3️⃣ Update step
        std::vector<std::vector<double>> new_centroids(
            k_, std::vector<double>(d, 0.0));
        std::vector<int> counts(k_, 0);

        for (int i = 0; i < n; i++) {
            int c = labels_[i];
            counts[c]++;
            for (int j = 0; j < d; j++) {
                new_centroids[c][j] += data[i][j];
            }
        }

        for (int c = 0; c < k_; c++) {
            if (counts[c] == 0) continue;
            for (int j = 0; j < d; j++) {
                new_centroids[c][j] /= counts[c];
            }
        }

        centroids_ = new_centroids;
    }
}

const std::vector<int>& KMeans::labels() const {
    return labels_;
}

const std::vector<std::vector<double>>& KMeans::centroids() const {
    return centroids_;
}
