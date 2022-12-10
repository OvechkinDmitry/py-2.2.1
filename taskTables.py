import re
import prettytable
from prettytable import PrettyTable
import csv
import doctest

first_row = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                     "Название региона", "Дата публикации вакансии"]

currency_to_rub = {"Манаты": 35.68,
                   "Белорусские рубли": 23.91,
                   "Евро": 59.90,
                   "Грузинский лари": 21.74,
                   "Киргизский сом": 0.76,
                   "Тенге": 0.13,
                   "Рубли": 1,
                   "Гривны": 1.64,
                   "Доллары": 60.66,
                   "Узбекский сум": 0.0055, }

interpreter = {"noExperience": "Нет опыта",
                "between1And3": "От 1 года до 3 лет",
                "between3And6": "От 3 до 6 лет",
                "moreThan6": "Более 6 лет",
                "AZN": "Манаты",
                "BYR": "Белорусские рубли",
                "EUR": "Евро",
                "GEL": "Грузинский лари",
                "KGS": "Киргизский сом",
                "KZT": "Тенге",
                "RUR": "Рубли",
                "UAH": "Гривны",
                "USD": "Доллары",
                "UZS": "Узбекский сум",
                "True": "Да",
                "False": "Нет",
                "FALSE": "Нет",
                "TRUE": "Да"}

parametrs = ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы",
                     "Премиум-вакансия","Идентификатор валюты оклада", "Название",
                     "Название региона", "Компания",""]
class DataSet:
    """Считывание файла и формирование структуры данных о нем.
        Attributes:
            name (str): название csv файла.
    """
    def __init__(self, name):
        """Инициализирует класс DataSet. Чтение фала,форматирование,вывод информации.
                Args:
                    name (str): название csv файла.
        """
        self.file_name = name
        self.interpreter = interpreter
        headings, vacancies = self.csv_reader()
        dictionaries = self.csv_filer(vacancies, headings)
        self.vacancies_objects = [Vacancy(dictionary) for dictionary in dictionaries]

    def csv_reader(self):
        '''Чтение данных из csv файла

        Returns:
            headings (list): список из заголовков фалйла
            vacancies (list): список из профессий
        '''
        headings = []
        vacancies = []
        columns = 0
        rows = 0
        is_headings = True
        with open(self.file_name, encoding="utf-8-sig") as File:
            reader = csv.reader(File)
            for row in reader:
                rows += 1
                if is_headings:
                    headings = row
                    columns = len(row)
                    is_headings = False
                else:
                    if "" not in row and len(row) == columns:
                        vacancies.append(row)
                    else: continue
        if rows < 2:
            print("Пустой файл" if rows == 0 else "Нет данных")
            exit()
        return headings, vacancies

    def csv_filer(self,reader, headings):
        """Записывает в словари данные полученные после чтения csv файла
        Args:
            reader (list): список вакансий полученных после обработки csv файла
            headings (list): список заголовков полученных после обработки csv файла
        Returns:
            dictionaries (list[dict]): список словарей с вакансиями
        """
        dictionaries = []
        for vacancy in reader:
            dictionary = {}
            for i in range(len(headings)):
                dictionary[headings[i]] = DataSet.format_str(self,vacancy[i])
            dictionaries.append(dictionary)
        return dictionaries

    @staticmethod
    def format_str(data, string):
        """Форматирует строки полученные из csv файла
        Args:
            string (str): строка полученная из csv файла
            >>> DataSet.format_str(DataSet('vacancies.csv'),'95000.0')
            '95000.0'

            >>> DataSet.format_str(DataSet('vacancies.csv'),'False')
            'Нет'

            >>> DataSet.format_str(DataSet('vacancies.csv'),'RUR')
            'Рубли'

            >>> DataSet.format_str(DataSet('vacancies.csv'),'between3And6')
            'От 3 до 6 лет'

            >>> DataSet.format_str(DataSet('vacancies.csv'),'Братск')
            'Братск'
        """
        string = re.compile(r'<[^>]+>').sub('', string)\
            .replace(" ", " ").replace(" ", " ")\
            .replace("  "," ").replace("  ", " ").strip()
        return data.interpreter[string] if string in data.interpreter else string


class Vacancy:
    '''
    Класс для предоставления вакансии
    Attributes:
        dictionary (dict): словарь
    '''
    def __init__(self, dictionary):
        '''
                Инициализирует объект вакансии. Выполняет структурирование информации о вакансии

                Attributes:
                        dictionary (dict): словарь с данными о вакансии
        '''
        self.dictionary = dictionary
        self.name = dictionary["name"]
        self.description = dictionary["description"]
        self.key_skills = dictionary["key_skills"]
        self.experience_id = dictionary["experience_id"]
        self.premium = dictionary["premium"]
        self.employer_name = dictionary["employer_name"]
        self.salary = Salary(dictionary["salary_from"], dictionary["salary_to"], dictionary["salary_gross"],
                             dictionary["salary_currency"])
        self.area_name = dictionary["area_name"]
        self.published_at = dictionary["published_at"]

    def get_value(self):
        """Возращает словарь с данными о вакансии

        Returns:
            (dict): словарь с данными о вакансии
        """
        return {"Название": self.name,
                "Описание": self.description,
                "Навыки": self.key_skills,
                "Опыт работы": self.experience_id,
                "Премиум-вакансия": self.premium,
                "Компания": self.employer_name,
                "Оклад": self.salary,
                "Название региона": self.area_name,
                "Дата публикации вакансии": self.published_at}

    def copy_vacancy(self):
        """Возращает копию вакансии

                Returns:
                    (Vacancy): объект вакансии
        """
        return Vacancy({"name": self.name, "description": self.description,
                        "key_skills": self.key_skills,
                        "experience_id": self.experience_id,
                        "premium": self.premium,
                        "employer_name": self.employer_name,
                        "salary_from": self.salary.salary_from,
                        "salary_to": self.salary.salary_to,
                        "salary_gross": self.salary.salary_gross,
                        "salary_currency": self.salary.salary_currency,
                        "area_name": self.area_name,
                        "published_at": self.published_at})


class Salary:
    """Информация о зарплате вакансии.
        Attributes:
            salary_from (int): Нижняя граница вилки оклада
            salary_to (int): Верхняя граница вилки оклада
            salary_gross (str): Оклад указан до вычета налогов
            salary_currency (str): Идентификатор валюты оклада
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """Инициализация объекта Salary. Перевод зарплаты в рубли (для последущего сравнения).
                Attributes:
                    salary_from (int): Нижняя граница вилки оклада
                    salary_to (int): Верхняя граница вилки оклада
                    salary_gross (str): Оклад указан до вычета налогов
                    salary_currency (str): Идентификатор валюты оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def get_salary(self):
        """Функция перевода валюты в рубли
              Returns:
                  (float): валюта в рублях
           >>> Salary(30000.0, 80000.0, 'Нет', 'Рубли').get_salary()
           55000.0
           >>> Salary(6000.0, 7000.0, 'Нет', 'Евро').get_salary()
           389350.0
           >>> Salary(20000.0, 30000.0, 'Нет', 'Киргизский сом').get_salary()
           19000.0
           >>> Salary(750000.0, 1500000.0, 'Нет', 'Тенге').get_salary()
           146250.0
           >>> Salary(70000.0, 80000.0, 'Да', 'Рубли').get_salary()
           75000.0
        """
        return (int(float(self.salary_from)) + int(float(self.salary_to))) / 2 * currency_to_rub[self.salary_currency]


class InputCorrect:
    """Проверка корректности ввода и существования файла.
        Attributes:
            filter_parametr (str): Параметр фильтрации.
            sort_parametr (str): Параметр сортировки.
            is_reversed (str): Обратная сортировка.
            span (str): Промежуток вывода.
            required_columns (str): Выводимые столбцы.
        """
    def __init__(self, filter_paremetr, sort_parametr, is_reversed, span, required_columns):##
        """Инициализация объекта InputCorrect. Проверка на ошибки ввода.
        Args:
            filter_parametr (str): Параметр фильтрации.
            sort_parametr (str): Параметр сортировки.
            is_reversed (str): Обратная сортировка.
            span (str): Промежуток вывода.
            required_columns (str): Выводимые столбцы.
            >>> InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет', '10 20', 'Название, Навыки, Опыт работы, Компания').is_reversed
            'Нет'
            >>> InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет', '10 20', 'Название, Навыки, Опыт работы, Компания').filter_parameter
            ['Опыт работы', 'От 3 до 6 лет']
            >>> InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет', '10 20', 'Название, Навыки, Опыт работы, Компания').span
            '10 20'
            >>> InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет', '10 20', 'Название, Навыки, Опыт работы, Компания').required_columns
            'Название, Навыки, Опыт работы, Компания'
        """
        self.filter_parameter = filter_paremetr.split(": ")
        self.sort_parametr = sort_parametr
        self.is_reversed = is_reversed
        self.span = span
        self.required_columns = required_columns

    def check_parameters(self):
        """Проверка на корректность вводимых данных
        """
        if len(self.filter_parameter) == 1 and self.filter_parameter[0] != "":
            print("Формат ввода некорректен")
            exit()
        elif self.filter_parameter[0] not in parametrs:
            print("Параметр поиска некорректен")
            exit()
        elif self.sort_parametr not in parametrs:
            print("Параметр сортировки некорректен")
            exit()
        elif self.is_reversed not in ["Да", "Нет", ""]:
            print("Порядок сортировки задан некорректно")
            exit()

    def sort_vacancies(self, vacancies):
        """Сортирует вакансии по указанным парметрам
        Args:
            vacancies list[Vacancy]: лист вакансий
        Returns:
            vacancies list[Vacancy]: отсортированный по парматрам лист с вакансиями
        """
        experience_dictionary = {"Нет опыта": 0, "От 1 года до 3 лет": 1, "От 3 до 6 лет": 2, "Более 6 лет": 3}
        self.is_reversed = True if self.is_reversed == "Да" else False
        if self.sort_parametr == "":
            vacancies = vacancies
        elif self.sort_parametr == "Оклад":
            vacancies = sorted(vacancies,
                                      key=lambda vacancy: vacancy.salary.get_salary(),
                                      reverse=self.is_reversed)
        elif self.sort_parametr == "Навыки":
            vacancies = sorted(vacancies,
                                      key=lambda vacancy: len(vacancy.key_skills.split("\n")),
                                      reverse=self.is_reversed)
        elif self.sort_parametr == "Опыт работы":
            vacancies = sorted(vacancies,
                                      key=lambda vacancy:
                                      experience_dictionary[vacancy.experience_id],
                                      reverse=self.is_reversed)
        else:
            vacancies = sorted(vacancies, key=lambda vacancy: vacancy.get_value()[self.sort_parametr],
                               reverse=self.is_reversed)
        return vacancies

    def filter_row(self, vacancy):
        """Осуществляет проверку на парметр фильтрации

        Args:
             vacancies (list[Vacancy]) : лист вакансий
        Returns:
              (bool): результат проверки
        """
        if self.filter_parameter[0] == "Оклад":
            if int(float(self.filter_parameter[1])) < int(float(vacancy.salary.salary_from))\
               or int(float(self.filter_parameter[1])) > int(float(vacancy.salary.salary_to)):
                return False
        elif self.filter_parameter[0] == "Дата публикации вакансии":
            if self.filter_parameter[1] != self.format_date(vacancy.published_at):
                return False
        elif self.filter_parameter[0] == "Навыки":
            for element in self.filter_parameter[1].split(", "):
                if element not in vacancy.key_skills.split("\n"):
                    return False
        elif self.filter_parameter[0] == "Идентификатор валюты оклада":
            if self.filter_parameter[1] != vacancy.salary.salary_currency:
                return False
        elif self.filter_parameter[0] in vacancy.get_value():
            if self.filter_parameter[1] != vacancy.get_value()[self.filter_parameter[0]]:
                return False
        return True

    def clip_table(self, table, count):
        """Обрезает таблицу

           Args:
              table: таблица
              count: кол-во необходимых столбцов

            Returns:
                (str): обрезанная таблица
        """
        self.span = self.span.split(" ")
        start = 0
        end = count
        if self.span[0] == "":
            pass
        elif len(self.span) == 1:
            start = int(self.span[0]) - 1
        elif len(self.span) == 2:
            start = int(self.span[0]) - 1
            end = int(self.span[1]) - 1
        self.required_columns = self.required_columns.split(", ")
        if self.required_columns[0] == "":
            return table.get_string(start=start, end=end)
        self.required_columns.insert(0, "№")
        return table.get_string(start=start, end=end, ﬁelds=self.required_columns)

    def print_vacancies(self, vacancies):
        """Печатает вакансии в виде таблицы PrettyTable.
        """
        table = PrettyTable(hrules=prettytable.ALL, align='l')
        counter = 1
        sorted_vacancies = self.sort_vacancies(vacancies)
        table.field_names = first_row
        for vacancy in sorted_vacancies:
            formatted_new_vacancy = InputCorrect.formatter(vacancy)
            if not self.filter_row(vacancy):
                continue
            row = [value if len(value) <= 100 else value[:100] + "..." for value in
                   formatted_new_vacancy.get_value().values()]
            row.insert(0, counter)
            table.add_row(row)
            counter += 1
        if counter == 1:
            print("Ничего не найдено")
            exit()
        table.max_width = 20
        table = self.clip_table(table, counter - 1)
        print(table)

    @staticmethod
    def formatter(vacancy):
        """Форматирует данные вакансии

        Returns :
            vacancies (list[Vacancy]) : лист вакансий с отформатированными полями
        """
        min_salary = InputCorrect.format_number(vacancy.salary.salary_from)
        max_salary = InputCorrect.format_number(vacancy.salary.salary_to)
        taxes = "Без вычета налогов" if vacancy.salary.salary_gross == "Да" else "С вычетом налогов"
        vacancy = vacancy.copy_vacancy()
        vacancy.salary = f"{min_salary} - {max_salary} ({vacancy.salary.salary_currency}) ({taxes})"
        vacancy.published_at = InputCorrect.format_date(vacancy.published_at)
        return vacancy

    @staticmethod
    def format_number(number):
        """Форматирует число

        Arg:
          number (float) : число для фоматирования
        Returns:
          new_number (str) : отформатированное число

        >>> InputCorrect.format_number(200000.0)
        '200 000'
        >>> InputCorrect.format_number(30000.0)
        '30 000'
        >>> InputCorrect.format_number(750000.0)
        '750 000'
        >>> InputCorrect.format_number(1500000.0)
        '1 500 000'
        >>> InputCorrect.format_number(29500.0)
        '29 500'
        """
        number = str(int(float(number)))
        first_digit_count = len(number) % 3
        triplets_count = len(number) // 3
        new_number = ""
        new_number += number[:first_digit_count]
        for i in range(triplets_count):
            if new_number != "":
                new_number += " "
            new_number += number[first_digit_count + i * 3: first_digit_count + (i + 1) * 3]
        return new_number
    @staticmethod
    def format_date(date):
        """
        >>> InputCorrect.format_date('2022-05-31T17:32:31+0300')
        '31.05.2022'
        >>> InputCorrect.format_date('2022-06-08T09:18:13+0300')
        '08.06.2022'
        >>> InputCorrect.format_date('2022-06-21T00:34:36+0300')
        '21.06.2022'
        >>> InputCorrect.format_date('2022-06-30T05:12:13+0300')
        '30.06.2022'
        """
        return date[8: 10] + "." + date[5: 7] + "." + date[: 4]
def getTable():
    file_name = input("Введите название файла: ")
    filter_attribute = input("Введите параметр фильтрации: ")
    sort_attribute = input("Введите параметр сортировки: ")
    need_to_reverse = input("Обратный порядок сортировки (Да / Нет): ")
    diapason = input("Введите диапазон вывода: ")
    needed_columns = input("Введите требуемые столбцы: ")
    input_correct = InputCorrect(filter_attribute, sort_attribute, need_to_reverse, diapason, needed_columns)
    input_correct.check_parameters()
    dataset = DataSet(file_name)
    input_correct.print_vacancies(dataset.vacancies_objects)

doctest.testmod()
# getTable()