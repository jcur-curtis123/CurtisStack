#ifndef CSV_READER_H
#define CSV_READER_H

#include <string>
#include <vector>
#include <fstream>

class CsvReader {
public:
    explicit CsvReader(const std::string& filename);
    bool readRow(std::vector<std::string>& row);

private:
    std::ifstream file_;
};

#endif
