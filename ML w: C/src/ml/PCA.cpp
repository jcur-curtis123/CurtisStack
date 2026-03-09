#include "PCA.h"
#include <cmath>
#include <random>

/// 
static std::vector<double> matVec(
    const std::vector<std::vector<double>>& M,
    const std::vector<double>& v) {

    std::vector<double> result(M.size(), 0.0);
    for (size_t i = 0; i < M.size(); i++) {
        for (size_t j = 0; j < v.size(); j++) {
            result[i] += M[i][j] * v[j];
        }
    }
    return result;
}

static double dot(const std::vector<double>& a,
                  const std::vector<double>& b) {
    double s = 0.0;
    for (size_t i = 0; i < a.size(); i++) {
        s += a[i] * b[i];
    }
    return s;
}
/// normalize data for cov matrix 
static void normalize(std::vector<double>& v) {
    double norm = std::sqrt(dot(v, v));
    for (double& x : v) x /= norm;
}

PCA::PCA(int n_components)
    : n_components_(n_components) {}

void PCA::fit(const std::vector<std::vector<double>>& data) {
    int n = data.size();
    int d = data[0].size();

    // Covariance matrix
    std::vector<std::vector<double>> cov(
        d, std::vector<double>(d, 0.0));

    for (const auto& row : data) {
        for (int i = 0; i < d; i++) {
            for (int j = 0; j < d; j++) {
                cov[i][j] += row[i] * row[j];
            }
        }
    }

    for (int i = 0; i < d; i++)
        for (int j = 0; j < d; j++)
            cov[i][j] /= n;

    components_.clear();

    // Power iteration for top components
    std::mt19937 gen(42);
    std::uniform_real_distribution<> dist(-1, 1);

    for (int c = 0; c < n_components_; c++) {
        std::vector<double> v(d);
        for (double& x : v) x = dist(gen);
        normalize(v);

        for (int iter = 0; iter < 100; iter++) {
            auto v_new = matVec(cov, v);
            normalize(v_new);
            v = v_new;
        }

        components_.push_back(v);

        // Deflation
        double lambda = dot(v, matVec(cov, v));
        for (int i = 0; i < d; i++)
            for (int j = 0; j < d; j++)
                cov[i][j] -= lambda * v[i] * v[j];
    }
}

std::vector<std::vector<double>>
PCA::transform(const std::vector<std::vector<double>>& data) const {

    std::vector<std::vector<double>> projected;

    for (const auto& row : data) {
        std::vector<double> z;
        for (const auto& comp : components_) {
            z.push_back(dot(row, comp));
        }
        projected.push_back(z);
    }
    return projected;
}
