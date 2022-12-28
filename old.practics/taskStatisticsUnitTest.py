from unittest import TestCase
from taskStatistics import *

dicts_for_test_two_same_one_diff = [{'name': 'Механик','published_at': 2022},
         {'name': 'Аналитик','published_at': 2022}
         ,{'name': 'Аналитик','published_at': 2020}]

dicts_for_test_three_same = [{'name': 'Аналитик','published_at': 2022},
         {'name': 'Аналитик','published_at': 2022},
         {'name': 'Аналитик','published_at': 2020}]



class taskTableUnitTests(TestCase):

    def test_get_vacancies_amount_in_cities_with_three_same(self):
        self.assertEqual(DataSet('vacancies.csv', 'Аналитик').get_vacancies_amount_in_cities([{'area_name': 'МСК'},
                                                                                              {'area_name': 'МСК'},
                                                                                              {'area_name': 'МСК'}]),{'МСК': 3})

    def test_get_vacancies_amount_in_cities_with_all_diff(self):
        self.assertEqual(DataSet('vacancies.csv', 'Аналитик').get_vacancies_amount_in_cities([{'area_name': 'МСК'},
                                                                                              {'area_name': 'ЕКБ'},
                                                                                              {'area_name': 'СПБ'}]),{'МСК': 1, 'ЕКБ': 1, 'СПБ': 1})

    def test_get_vacancies_amount_in_cities_with_two_same_one_diff(self):
        self.assertEqual(DataSet('vacancies.csv', 'Аналитик').get_vacancies_amount_in_cities([{'area_name': 'МСК'},
                                                                                              {'area_name': 'СПБ'},
                                                                                              {'area_name': 'СПБ'}]),{'МСК': 1, 'СПБ': 2} )

    def test_get_vacancies_amount_in_cities_with_empty(self):
        self.assertEqual( DataSet('vacancies.csv', 'Аналитик').get_vacancies_amount_in_cities([]), {})

    def test_get_vacancies_amount_at_times_for_profession_with_empty(self):
        self.assertEqual(DataSet('vacancies.csv','Аналитик').get_vacancies_amount_at_times_for_profession([]),{2022: 0})

    def test_vacancies_amount_at_times_for_profession_with_two_same_one_diff(self):
        self.assertEqual(DataSet('vacancies.csv','Аналитик').get_vacancies_amount_at_times_for_profession(dicts_for_test_two_same_one_diff),
                         {2020: 1, 2022: 1})

    def test_vacancies_amount_at_times_for_profession_with_three_same(self):
        self.assertEqual(DataSet('vacancies.csv','Аналитик').get_vacancies_amount_at_times_for_profession(dicts_for_test_three_same),
                         {2020: 1, 2022: 2})





    def test_get_vacancies_amount_at_time_with_all_diff(self):
        self.assertEqual(DataSet.get_vacancies_amount_at_times([2022, 2019, 2022, 2021]), {2019: 1, 2021: 1, 2022: 2})

    def test_get_vacancies_amount_at_time_with_all_same(self):
        self.assertEqual(DataSet.get_vacancies_amount_at_times([2022, 2022, 2022,2022]), {2022: 4})

    def test_get_vacancies_amount_at_time_with_more_diff(self):
        self.assertEqual(DataSet.get_vacancies_amount_at_times([2007, 2010, 2007, 2001, 2005, 1992, 1999]),
                         {1992: 1, 1999: 1, 2001: 1, 2005: 1, 2007: 2, 2010: 1})

    def test_get_vacancies_amount_at_time_with_empty(self):
        self.assertEqual(DataSet.get_vacancies_amount_at_times([]), {})


    def test_vacancy_fields_with_salary(self):
        self.assertEqual(Vacancy({'name': '',
                                  'salary_from': '26000.0',
                                  'salary_to': '35000.0',
                                  'salary_currency': 'RUR',
                                  'area_name': '',
                                  'published_at': '2022'}).salary, 30500.0)

    def test_vacancy_fields_with_published_at(self):
        self.assertEqual(Vacancy({'name': '',
                                  'salary_from': '0',
                                  'salary_to': '0',
                                  'salary_currency': 'RUR',
                                  'area_name': '',
                                  'published_at': '2022'}).published_at, 2022)

    def test_vacancy_fields_with_area_name(self):
        self.assertEqual(Vacancy({'name': '',
                                  'salary_from': '0',
                                  'salary_to': '0',
                                  'salary_currency': 'RUR',
                                  'area_name': 'Краснотурьинск',
                                  'published_at': '2022'}).area_name, 'Краснотурьинск')

    def test_vacancy_fields_with_name(self):
        self.assertEqual(Vacancy({'name': 'Техник по связи г. Краснотурьинск',
                                  'salary_from': '0',
                                  'salary_to': '0',
                                  'salary_currency': 'RUR',
                                  'area_name': '',
                                  'published_at': '2022'}).name, 'Техник по связи г. Краснотурьинск')

    def test_take_first_ten_with_empty(self):
        self.assertEqual(take_first_ten({}), {})

    def test_take_first_ten_with_less_than_ten(self):
        self.assertEqual(take_first_ten({'Казань': 156337, 'Москва': 142291, 'Санкт-Петербург': 111548, 'Уфа': 106750}),
                         {'Казань': 156337, 'Москва': 142291, 'Санкт-Петербург': 111548, 'Уфа': 106750})

    def test_take_first_ten_with_more_than_ten(self):
        self.assertEqual(take_first_ten({'Казань': 156337,
                                         'Москва': 142291,
                                         'Санкт-Петербург': 111548,
                                         'Уфа': 106750,
                                         'Екатеринбург': 95270,
                                         'Владивосток': 87916,
                                         'Набережные Челны': 81142,
                                         'Иркутск': 80357,
                                         'Нижний Новгород': 74437,
                                         'Краснодар': 70402,
                                         'Ростов-на-Дону': 68961,
                                         'Хабаровск': 62800,
                                         'Алматы': 61152,
                                         'Тюмень': 59900,
                                         'Ижевск': 58200,
                                         'Красноярск': 57833,
                                         'Новосибирск': 56958,
                                         'Пермь': 55888,
                                         'Челябинск': 52402,
                                         'Томск': 46225,
                                         'Минск': 45560}), {'Казань': 156337,
                                                            'Москва': 142291,
                                                            'Санкт-Петербург': 111548,
                                                            'Уфа': 106750,
                                                            'Екатеринбург': 95270,
                                                            'Владивосток': 87916,
                                                            'Набережные Челны': 81142,
                                                            'Иркутск': 80357,
                                                            'Нижний Новгород': 74437,
                                                            'Краснодар': 70402})

