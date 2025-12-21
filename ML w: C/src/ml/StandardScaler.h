#ifndef STANDARD_SCALER_H
#define STANDARD_SCALER_H

#include <vector>

class StandardScaler {
public:
    void fit(const std::vector<std::vector<double>>& data);
    std::vector<std::vector<double>> transform(
        const std::vector<std::vector<double>>& data) const;

private:
    std::vector<double> means_;
    std::vector<double> stds_;
};

#endif
