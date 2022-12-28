import shutil
import csv
import os


def format_year(date):
    """Функция для форматирования года
        Args:
            date (str): дата в виде строки
        Returns:
            str: отформатированная дата
    """
    return date[:4]

class DataSet_Separator:
    """Считывание файла и формирование удобной структуры данных.

        Attributes:
            file_name (str): название csv файла.
            dir_name (str): Папка расположения CSV-файлов.
    """
    def __init__(self, file_name, dir_name):
        """Инициализация класса DataSet. Чтение. Разделение на разные файлы.
        Args:
            file_name (str): Неразделенный файл и его первая строка.
            dir_name (str): Папка расположения CSV-файлов.
        """
        self.file_name = file_name
        self.dir_name = dir_name
        self.csv_reader()
        self.separate_csv()

    def csv_reader(self):
        """Чтение файла и отсеивание невалидных строк"""
        with open(self.file_name, "r", encoding="utf-8-sig") as csv_file:
            file = csv.reader(csv_file)
            self.headings = next(file)
            self.vacancies_rows = [row for row in file
                                   if not ("" in row) and len(row) == len(self.headings)]


    def write_csv(self, year, rows):
        """Создает csv-файл и записывает в него данные по конкретному году

        Args:
            year (str): год.
            rows (list): Список вакансий этого года.
        """
        path = f"{self.dir_name}/vacancies_{year}.csv"
        with open(path, "a", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def separate_csv(self):
        """Разделяет данные на csv-файлы по годам"""
        rows_by_years = [[]]
        index = 0
        year_index = self.headings.index("published_at")
        current_year = format_year(self.vacancies_rows[0][year_index])
        for row in self.vacancies_rows:
            year_of_row = format_year(row[year_index])
            if year_of_row == current_year:
                rows_by_years[index].append(row)
            else:
                self.write_csv(current_year, rows_by_years[index])
                index += 1
                current_year = year_of_row
                rows_by_years.append([])
        self.write_csv(current_year, rows_by_years[index])


def separate_file_csv(dir_name):
    """Разделяет исходный csv файла по годам
    Args:
        dir_name (str): название папки где будут расположены csv файлы
    """
    file_name = input("Введите название файла: ")
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    return DataSet_Separator(file_name, dir_name)


separate_file_csv("csv_by_years")
