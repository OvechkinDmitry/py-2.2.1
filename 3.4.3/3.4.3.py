import os
import pathlib
import concurrent.futures
import re
import pandas as pd
from dataForPdfExcel import Statistic
from getExcelPdf import StatisticFilesMaker



class InitData:
    """Класс для создания начальных данных"""
    def __init__(self):
        """инициализирует InitData"""
        self.year_salary = {}
        self.year_vacancy = {}
        self.professions_year_salary = {}
        self.professions_year_vacancies = {}


class CsvDevider:
    """ Класс для раделения набора вакансий по годам """
    def __init__(self, file_name, directory):
        """инициализирует CsvDevider

        :param file_name: имя файла
        :param directory: название папки
        """
        csv_reader = pd.read_csv(file_name).to_dict("records")
        self.dir_name = directory
        self.headlines, self.vacancies = [csv_reader[0].keys()], [row.values() for row in csv_reader[1:]]
        self.format_rows(self.headlines, self.vacancies)

    def format_rows(self, headlines, vacancies, cur_year="0"):
        """Форматирует вакансии и загаловки"""
        self.first_vacancy = ""
        os.mkdir(self.dir_name)
        vacancies_cur_year = []
        for vacancy in vacancies:
            if (len(vacancy) == len(headlines)) and \
                    ((all([v != "" for v in vacancy])) or
                    (vacancy[1] == "" and vacancy[2] != "") or (vacancy[1] != "" and vacancy[2] == "")):
                vacancy = [" ".join(re.sub("<.*?>", "", value).replace('\n', '; ').split()) for value in vacancy]
                if len(self.first_vacancy) == 0 : self.first_vacancy = vacancy
                if vacancy[-1][:4] != cur_year:
                    if len(vacancies_cur_year) != 0:
                        vacancies = pd.DataFrame(vacancies, columns=headlines)
                        vacancies.to_csv(f'{self.dir_name}/vacancies_{cur_year}.csv', index=False)
                        vacancies_cur_year.clear()
                    cur_year = vacancy[-1][:4]
                vacancies_cur_year.append([v for v in vacancy])
                self.last_vacancy = vacancy
        vacancies = pd.DataFrame(vacancies, columns=headlines)
        vacancies.to_csv(f'{self.dir_name}/vacancies_{cur_year}.csv', index=False)


if __name__ == "__main__":
    init_data = InitData()
    file_name = input("Введите название файла: ")
    prof_name = input("Введите название профессии: ")
    CsvDevider('vacancies_by_year')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        elems = list(executor.map(Statistic(prof_name).get_data, [str(file)
                                                                  for file in
                                                                  pathlib.Path(f"./'vacancies_by_year'").iterdir()]))
        for el in elems:
            for i, value in zip(range(4), [init_data.year_salary,init_data.year_vacancy,
                                           init_data.professions_year_salary,init_data.professions_year_vacancies]):
                value.update(el[i])
    StatisticFilesMaker(init_data.year_salary, init_data.year_vacancy,
                        init_data.professions_year_salary,
                        init_data.professions_year_vacancies, prof_name).create_files()
