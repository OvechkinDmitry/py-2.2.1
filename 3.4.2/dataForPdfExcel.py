from dataSet import Salary
from dataSet import DataSet


class Statistic:
    """Класс для обработки, иницилизации данных  представления статистики"""
    def __init__(self, profession):
        self.profession = profession

    def get_data(self, file_name):
        """Обработка данных

        :param file_name: название файла
        :return: поля для формирования статистики
        """
        data = DataSet(file_name).vacancies_objects
        data_profession = [d for d in data if self.profession in d.name]
        year_salary = self.vacancy_to_salary(data)
        professions_year_salary = self.fill_empty_years(self.vacancy_to_salary(data_profession), year_salary)
        year_salary, year_vacancy = self.salary_to_dict(year_salary)
        professions_year_salary, professions_year_vacancies = self.salary_to_dict(professions_year_salary)
        return year_salary, year_vacancy, professions_year_salary, professions_year_vacancies

    def vacancy_to_salary(self, vacancies):
        """Конвертация в массив зарплат для вакансий

        :param vacancies: объекты вакансий
        :return: массив зарплат
        """
        param_salary = {}
        for vacancy in vacancies:
            if not param_salary.__contains__(vacancy.year):
                param_salary[vacancy.year] = SalaryFromYear(vacancy.year, vacancy.salary)
            else:
                param_salary[vacancy.year] = param_salary[vacancy.year].add_salary(vacancy.salary)
        return [param_salary[d] for d in param_salary]

    def salary_to_dict(self, param_salary):
        """Конвертация зарплаты словарь

        :param param_salary:
        :return:
        """
        return {x: y for x, y in zip([int(r.param) for r in param_salary],
                                     [0 if v.count_vacancies == 0 else int(v.salary / v.count_vacancies) for v in
                                      param_salary])}, \
               {x: y for x, y in zip([int(r.param) for r in param_salary], [v.count_vacancies for v in param_salary])}

    def fill_empty_years(self, param_salary, year_salary):
        """Заполняет отстутствующие года нулевой зарплатой

        :param param_salary: зарплата
        :param year_salary: год
        :return:
        """
        years = [i.param for i in year_salary]
        s_years = [el.param for el in param_salary]
        for y in years:
            if y not in s_years:
                param_salary.insert(int(y) - int(years[0]),
                                    SalaryFromYear(y, Salary("0", "0", "RUR", "2003-10-07T00:00:00+0400")))
                param_salary[int(y) - int(years[0])].count_vacancies = 0
        return param_salary

class SalaryFromYear:
    """Класс для представления параметра и связанной с ним зарплаты"""
    def __init__(self, param, salary):
        self.param = param
        self.salary = salary.get_average()
        self.count_vacancies = 1


    def add_salary(self, new_salary):
        """Добавляет среднее значение к заплате и увеличивает среднее значение

        :param new_salary: зарплата
        :return: объект класса SalaryFromYear
        """
        self.count_vacancies += 1
        self.salary += new_salary.get_average()
        return self
