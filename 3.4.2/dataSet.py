import re
import pandas as pd


class Salary:
    """Класс для представления зарплат"""
    def __init__(self, salary_from, salary_to, salary_currency, published_at):
        self.salary_from = self.check_field(salary_from)
        self.salary_to = self.check_field(salary_to)
        self.salary_currency = salary_currency
        self.published_at = published_at
        self.month_year = f"{self.published_at[5:7]}/{self.published_at[:4]}"

    #проверка поля
    check_field = lambda self, x: 0 if type(x) == str and x == "" else float(x)

    #вычисление среднего значения и округления до 4 знаков
    get_average = lambda self: round(((self.salary_from + self.salary_to) * self.get_constant()) / 2, 4)

    def get_constant(self):
        """Вычисляет константу для валюты

        :return: константа для валюты
        """
        currencies = pd.read_csv("currencies.csv")
        currency = currencies.loc[currencies["date"] == self.month_year]
        if currency.__contains__(self.salary_currency):
            return float(currency[self.salary_currency])
        return 0 if self.salary_currency != "RUR" else 1

class Vacancy:
    """Класс для представления вакансий"""
    def __init__(self, vacancy):
        """Инициализирует Vacancy

        :param vacancy: данные о вакансии
        """
        self.name = vacancy["name"]
        self.salary = Salary(salary_from=vacancy["salary_from"],
                             salary_to=vacancy["salary_to"],
                             salary_currency=vacancy["salary_currency"],
                             published_at=vacancy["published_at"])
        self.area_name = vacancy["area_name"]
        self.published_at = vacancy["published_at"]
        self.year = self.published_at[:4]

    #получение листа с информацией о вакансии
    get_vacancy_list = lambda self: [self.name, self.salary.get_average(), self.area_name, self.published_at]



class DataSet:
    """Класс для представления набора вакансий"""
    def __init__(self, file_name: str):
        """Инициализирует DataSet"""
        self.file_name = file_name
        self.csv_reader = pd.read_csv(self.file_name)
        headings, vacancies = [self.csv_reader[0].keys()], [row.values() for row in self.csv_reader[1:]]
        self.vacancies_objects = self.formatter(headings, vacancies)

    def formatter(self, headlines, vacancies):
        """Отбирает правильно заполненные вакансии и конвертирует в класс Vacancy"""
        result = []
        for vacancy in vacancies:
            vacancy = [" ".join(re.sub("<.*?>", "", value).replace('\n', '; ').split()) for value in vacancy]
            result.append(Vacancy({x: y for x, y in zip([r for r in headlines], [v for v in vacancy])}))
        return result

