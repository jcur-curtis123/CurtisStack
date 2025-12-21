#include "StandardScaler.h"
#include <cmath>

void StandardScaler::fit(const std::vector<std::vector<double>>& data) {
    size_t n = data.size();
    size_t d = data[0].size();

    means_.assign(d, 0.0);
    stds_.assign(d, 0.0);

    // Compute means
    for (const auto& row : data) {
        for (size_t j = 0; j < d; j++) {
            means_[j] += row[j];
        }
    }
    for (size_t j = 0; j < d; j++) {
        means_[j] /= n;
    }

    // Compute standard deviations
    for (const auto& row : data) {
        for (size_t j = 0; j < d; j++) {
            double diff = row[j] - means_[j];
            stds_[j] += diff * diff;
        }
    }
    for (size_t j = 0; j < d; j++) {
        stds_[j] = std::sqrt(stds_[j] / n);
        if (stds_[j] == 0.0) stds_[j] = 1.0;
    }
}

std::vector<std::vector<double>>
StandardScaler::transform(const std::vector<std::vector<double>>& data) const {
    std::vector<std::vector<double>> scaled = data;

    for (auto& row : scaled) {
        for (size_t j = 0; j < row.size(); j++) {
            row[j] = (row[j] - means_[j]) / stds_[j];
        }
    }
    return scaled;
}
