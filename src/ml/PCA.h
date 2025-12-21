#ifndef PCA_H
#define PCA_H

#include <vector>

class PCA {
public:
    explicit PCA(int n_components);

    void fit(const std::vector<std::vector<double>>& data);
    std::vector<std::vector<double>> transform(
        const std::vector<std::vector<double>>& data) const;

private:
    int n_components_;
    std::vector<std::vector<double>> components_;
};

#endif
