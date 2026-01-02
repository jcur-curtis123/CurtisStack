#ifndef KMEANS_H
#define KMEANS_H

#include <vector>
/// def KMeans for 
class KMeans {
public:
    KMeans(int k, int max_iters = 100);

    void fit(const std::vector<std::vector<double>>& data);

    const std::vector<int>& labels() const;
    const std::vector<std::vector<double>>& centroids() const;

private:
    int k_;
    int max_iters_;

    std::vector<int> labels_;
    std::vector<std::vector<double>> centroids_;

    double distance(const std::vector<double>& a,
                    const std::vector<double>& b);
};

#endif
