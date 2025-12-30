#ifndef DATABASE_H
#define DATABASE_H

#include <sqlite3.h>
#include <string>
#include <vector>

class Database {
public:
    explicit Database(const std::string& filename);
    ~Database();

    void execute(const std::string& sql);

    sqlite3* raw();   // expose raw SQLite handle

    // NEW: query housing data into a numeric matrix
    std::vector<std::vector<double>> queryHousingData();

private:
    sqlite3* db_;
};

#endif
