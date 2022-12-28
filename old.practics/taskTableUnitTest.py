from unittest import TestCase
from taskTables import *

class taskTableUnitTests(TestCase):
    def test_format_str_with_ordinary_number(self):
        self.assertEqual(DataSet.format_str(DataSet('vacancies.csv'), '95000.0'), '95000.0')

    def test_format_str_with_bool(self):
        self.assertEqual(DataSet.format_str(DataSet('vacancies.csv'),'False'), 'Нет')

    def test_format_str_with_currency(self):
        self.assertEqual(DataSet.format_str(DataSet('vacancies.csv'), 'RUR'), 'Рубли')

    def test_format_str_with_inrepreted_string(self):
        self.assertEqual(DataSet.format_str(DataSet('vacancies.csv'), 'between3And6'), 'От 3 до 6 лет')

    def test_format_str_with_ordinary_sting(self):
        self.assertEqual(DataSet.format_str(DataSet('vacancies.csv'), 'Братск'), 'Братск')


    def test_get_salary_with_rubles_one(self):
        self.assertEqual(Salary(30000.0, 80000.0, 'Нет', 'Рубли').get_salary(), 55000.0)

    def test_get_salary_with_euro(self):
        self.assertEqual(Salary(6000.0, 7000.0, 'Нет', 'Евро').get_salary(), 389350.0)

    def test_get_salary_with_kz_som(self):
        self.assertEqual(Salary(20000.0, 30000.0, 'Нет', 'Киргизский сом').get_salary(), 19000.0)

    def test_get_salary_with_tenge(self):
        self.assertEqual(Salary(750000.0, 1500000.0, 'Нет', 'Тенге').get_salary(), 146250.0)

    def test_get_salary_with_rubles_two(self):
        self.assertEqual(Salary(70000.0, 80000.0, 'Да', 'Рубли').get_salary(), 75000.0)

    def test_inputCorrect_with_reversed(self):
        self.assertEqual(InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет',
                                      '10 20', 'Название, Навыки, Опыт работы, Компания').is_reversed, 'Нет')

    def test_inputCorrect_filter_parameter(self):
        self.assertEqual(InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет',
                                      '10 20', 'Название, Навыки, Опыт работы, Компания').filter_parameter,
                                      ['Опыт работы', 'От 3 до 6 лет'])

    def test_inputCorrect_with_span(self):
        self.assertEqual(InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет',
                                      '10 20', 'Название, Навыки, Опыт работы, Компания').span, '10 20')

    def test_inputCorrect_with_required_columns(self):
        self.assertEqual(InputCorrect('Опыт работы: От 3 до 6 лет', 'Оклад', 'Нет',
                                      '10 20', 'Название, Навыки, Опыт работы, Компания').required_columns,
                                       'Название, Навыки, Опыт работы, Компания')


    def test_format_number_with_200000(self):
        self.assertEqual(InputCorrect.format_number(200000.0), '200 000')

    def test_format_number_with_30000(self):
        self.assertEqual(InputCorrect.format_number(30000.0), '30 000')

    def test_format_number_with_750000(self):
        self.assertEqual(InputCorrect.format_number(750000.0), '750 000')

    def test_format_number_with_1500000(self):
        self.assertEqual(InputCorrect.format_number(1500000.0), '1 500 000')

    def test_format_number_with_29500(self):
        self.assertEqual(InputCorrect.format_number(29500.0), '29 500')



    def test_format_date_with_date_one(self):
        self.assertEqual(InputCorrect.format_date('2022-05-31T17:32:31+0300'), '31.05.2022')

    def test_format_date_with_date_two(self):
        self.assertEqual(InputCorrect.format_date('2022-06-08T09:18:13+0300'), '08.06.2022')

    def test_format_date_with_date_three(self):
        self.assertEqual(InputCorrect.format_date('2022-06-21T00:34:36+0300'), '21.06.2022')

    def test_format_date_with_date_four(self):
        self.assertEqual(InputCorrect.format_date('2022-06-30T05:12:13+0300'), '30.06.2022')

