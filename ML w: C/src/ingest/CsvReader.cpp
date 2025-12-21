#include "CsvReader.h"
#include <sstream>

CsvReader::CsvReader(const std::string& filename)
    : file_(filename) {}

bool CsvReader::readRow(std::vector<std::string>& row) {
    row.clear();

    std::string line;
    if (!std::getline(file_, line)) {
        return false;
    }

    std::stringstream ss(line);
    std::string cell;

    while (std::getline(ss, cell, ',')) {
        row.push_back(cell);
    }

    return true;
}
