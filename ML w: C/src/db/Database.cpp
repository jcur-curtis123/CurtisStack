#include "Database.h"
#include <iostream>

Database::Database(const std::string& filename) : db_(nullptr) {
    if (sqlite3_open(filename.c_str(), &db_) != SQLITE_OK) {
        std::cerr << "Failed to open database: "
                  << sqlite3_errmsg(db_) << std::endl;
        db_ = nullptr;
    }
}

Database::~Database() {
    if (db_) {
        sqlite3_close(db_);
    }
}

void Database::execute(const std::string& sql) {
    char* errMsg = nullptr;

    if (sqlite3_exec(db_, sql.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
        std::cerr << "SQL error: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    }
}

sqlite3* Database::raw() {
    return db_;
}


std::vector<std::vector<double>> Database::queryHousingData() {
    std::vector<std::vector<double>> data;

    const char* sql =
        "SELECT price, area, bedrooms, bathrooms, stories, parking, "
        "mainroad, guestroom, basement, hotwaterheating, "
        "airconditioning, prefarea, furnishingstatus "
        "FROM housing;";

    sqlite3_stmt* stmt;
    sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::vector<double> row;
        for (int i = 0; i < 13; i++) {
            row.push_back(sqlite3_column_double(stmt, i));
        }
        data.push_back(row);
    }

    sqlite3_finalize(stmt);
    return data;
}