#include <iostream>
#include "db/Database.h"
#include "ml/StandardScaler.h"
#include "ml/KMeans.h"
#include "ml/PCA.h"

int main() {
    Database db("housing.db");

    auto data = db.queryHousingData();

    StandardScaler scaler;
    scaler.fit(data);
    auto scaled = scaler.transform(data);

    // K-Means
    KMeans kmeans(3);
    kmeans.fit(scaled);

    // PCA
    PCA pca(2);
    pca.fit(scaled);
    auto projected = pca.transform(scaled);

    std::cout << "First 5 PCA projections:\n";
    for (int i = 0; i < 5; i++) {
        std::cout << projected[i][0] << ", "
                  << projected[i][1] << "\n";
    }

    return 0;
}

