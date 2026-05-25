#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <limits>

using namespace std;

struct StudentGroup {
    string name;
    int year;
    char level;
    string faculty;
    string headman;
    int studentsCount;

    string toCSV() const {
        return name + "," +
               to_string(year) + "," +
               string(1, level) + "," +
               faculty + "," +
               headman + "," +
               to_string(studentsCount);
    }

    static StudentGroup fromCSV(const string& line) {
        StudentGroup group;
        string yearStr, levelStr, countStr;

        stringstream ss(line);

        getline(ss, group.name, ',');
        getline(ss, yearStr, ',');
        getline(ss, levelStr, ',');
        getline(ss, group.faculty, ',');
        getline(ss, group.headman, ',');
        getline(ss, countStr, ',');

        group.year = stoi(yearStr);
        group.level = levelStr[0];
        group.studentsCount = stoi(countStr);

        return group;
    }
};

class StudentGroupDatabase {
private:
    vector<StudentGroup> groups;

    void printHeader() const {
        cout << left
             << setw(5)  << "№"
             << setw(20) << "Группа"
             << setw(10) << "Год"
             << setw(10) << "Тип"
             << setw(20) << "Факультет"
             << setw(20) << "Староста"
             << setw(10) << "Кол-во"
             << endl;

        cout << string(95, '-') << endl;
    }

    void printGroup(const StudentGroup& group, int index) const {
        cout << left
             << setw(5)  << index
             << setw(20) << group.name
             << setw(10) << group.year
             << setw(10) << group.level
             << setw(20) << group.faculty
             << setw(20) << group.headman
             << setw(10) << group.studentsCount
             << endl;
    }

public:
    void loadFromFile(const string& filename) {
        ifstream file(filename);

        if (!file.is_open()) {
            cout << "Не удалось открыть файл.\n";
            return;
        }

        groups.clear();

        string line;
        getline(file, line);

        while (getline(file, line)) {
            if (!line.empty()) {
                try {
                    groups.push_back(StudentGroup::fromCSV(line));
                } catch (...) {
                    cout << "Ошибка чтения строки: " << line << endl;
                }
            }
        }

        file.close();
        cout << "База данных загружена.\n";
    }

    void saveToFile(const string& filename) const {
        ofstream file(filename);

        if (!file.is_open()) {
            cout << "Не удалось сохранить файл.\n";
            return;
        }

        file << "Name,Year,Level,Faculty,Headman,StudentsCount\n";

        for (const StudentGroup& group : groups) {
            file << group.toCSV() << endl;
        }

        file.close();
        cout << "База данных сохранена.\n";
    }

    void showAll() const {
        if (groups.empty()) {
            cout << "База данных пуста.\n";
            return;
        }

        printHeader();

        for (size_t i = 0; i < groups.size(); i++) {
            printGroup(groups[i], i + 1);
        }
    }

    void addGroup() {
        StudentGroup group;

        cout << "Название группы: ";
        getline(cin >> ws, group.name);

        cout << "Год набора: ";
        cin >> group.year;

        cout << "Тип обучения (B/S/M): ";
        cin >> group.level;

        cout << "Факультет: ";
        getline(cin >> ws, group.faculty);

        cout << "Староста: ";
        getline(cin >> ws, group.headman);

        cout << "Количество студентов: ";
        cin >> group.studentsCount;

        groups.push_back(group);

        cout << "Запись добавлена.\n";
    }

    void deleteGroup() {
        int number;

        cout << "Введите номер записи: ";
        cin >> number;

        if (number < 1 || number > static_cast<int>(groups.size())) {
            cout << "Неверный номер записи.\n";
            return;
        }

        groups.erase(groups.begin() + number - 1);

        cout << "Запись удалена.\n";
    }

    void sortByName() {
        sort(groups.begin(), groups.end(), [](const StudentGroup& a, const StudentGroup& b) {
            return a.name < b.name;
        });

        cout << "База отсортирована по названию группы.\n";
    }

    void searchByName() const {
        string name;

        cout << "Введите название группы: ";
        getline(cin >> ws, name);

        bool found = false;

        printHeader();

        for (size_t i = 0; i < groups.size(); i++) {
            if (groups[i].name == name) {
                printGroup(groups[i], i + 1);
                found = true;
            }
        }

        if (!found) {
            cout << "Группа не найдена.\n";
        }
    }

    void filterByYearRange() const {
        int startYear, endYear;

        cout << "Начальный год: ";
        cin >> startYear;

        cout << "Конечный год: ";
        cin >> endYear;

        bool found = false;

        printHeader();

        for (size_t i = 0; i < groups.size(); i++) {
            if (groups[i].year >= startYear && groups[i].year <= endYear) {
                printGroup(groups[i], i + 1);
                found = true;
            }
        }

        if (!found) {
            cout << "Записи не найдены.\n";
        }
    }

    void showFacultyGroupsSortedByCount() const {
        string faculty;

        cout << "Введите факультет: ";
        getline(cin >> ws, faculty);

        vector<StudentGroup> result;

        copy_if(groups.begin(), groups.end(), back_inserter(result),
            [&](const StudentGroup& group) {
                return group.faculty == faculty;
            });

        sort(result.begin(), result.end(), [](const StudentGroup& a, const StudentGroup& b) {
            return a.studentsCount < b.studentsCount;
        });

        if (result.empty()) {
            cout << "Группы этого факультета не найдены.\n";
            return;
        }

        printHeader();

        for (size_t i = 0; i < result.size(); i++) {
            printGroup(result[i], i + 1);
        }
    }

    void splitByLevel() const {
        ofstream bachelor("bachelor.csv");
        ofstream specialist("specialist.csv");
        ofstream master("master.csv");

        string header = "Name,Year,Level,Faculty,Headman,StudentsCount\n";

        bachelor << header;
        specialist << header;
        master << header;

        for (const StudentGroup& group : groups) {
            if (group.level == 'B' || group.level == 'b') {
                bachelor << group.toCSV() << endl;
            } else if (group.level == 'S' || group.level == 's') {
                specialist << group.toCSV() << endl;
            } else if (group.level == 'M' || group.level == 'm') {
                master << group.toCSV() << endl;
            }
        }

        bachelor.close();
        specialist.close();
        master.close();

        cout << "База разделена на bachelor.csv, specialist.csv и master.csv.\n";
    }
};

void showMenu() {
    cout << "\n===== МЕНЮ =====\n";
    cout << "1. Загрузить БД из файла\n";
    cout << "2. Показать БД\n";
    cout << "3. Добавить запись\n";
    cout << "4. Удалить запись\n";
    cout << "5. Сохранить БД в файл\n";
    cout << "6. Сортировать по названию группы\n";
    cout << "7. Найти группу по названию\n";
    cout << "8. Выборка по диапазону годов\n";
    cout << "9. Группы факультета по численности\n";
    cout << "10. Разделить БД по типу обучения\n";
    cout << "0. Выход\n";
    cout << "Выберите пункт: ";
}

int main() {
    setlocale(LC_ALL, "Russian");

    StudentGroupDatabase database;
    int choice;
    string filename;

    do {
        showMenu();

        if (!(cin >> choice)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Ошибка ввода. Введите число.\n";
            continue;
        }

        switch (choice) {
            case 1:
                cout << "Введите имя CSV-файла: ";
                cin >> filename;
                database.loadFromFile(filename);
                break;

            case 2:
                database.showAll();
                break;

            case 3:
                database.addGroup();
                break;

            case 4:
                database.deleteGroup();
                break;

            case 5:
                cout << "Введите имя CSV-файла: ";
                cin >> filename;
                database.saveToFile(filename);
                break;

            case 6:
                database.sortByName();
                break;

            case 7:
                database.searchByName();
                break;

            case 8:
                database.filterByYearRange();
                break;

            case 9:
                database.showFacultyGroupsSortedByCount();
                break;

            case 10:
                database.splitByLevel();
                break;

            case 0:
                cout << "Выход из программы.\n";
                break;

            default:
                cout << "Неверный пункт меню.\n";
        }

    } while (choice != 0);

    return 0;
}