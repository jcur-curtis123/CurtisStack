#include "HousingRecord.h"
#include "CsvReader.h"
#include "../db/Database.h"
#include <vector>
#include <string>
#include <iostream>

int yesNoToInt(const std::string& s) {
    return (s == "yes") ? 1 : 0;
}

int furnishingToInt(const std::string& s) {
    if (s == "unfurnished") return 0;
    if (s == "semi-furnished") return 1;
    return 2;
}

HousingRecord parseRecord(const std::vector<std::string>& row) {
    HousingRecord r;

    r.price = std::stod(row[0]);
    r.area = std::stod(row[1]);
    r.bedrooms = std::stoi(row[2]);
    r.bathrooms = std::stoi(row[3]);
    r.stories = std::stoi(row[4]);
    r.mainroad = yesNoToInt(row[5]);
    r.guestroom = yesNoToInt(row[6]);
    r.basement = yesNoToInt(row[7]);
    r.hotwaterheating = yesNoToInt(row[8]);
    r.airconditioning = yesNoToInt(row[9]);
    r.parking = std::stoi(row[10]);
    r.prefarea = yesNoToInt(row[11]);
    r.furnishingstatus = furnishingToInt(row[12]);

    return r;
}
