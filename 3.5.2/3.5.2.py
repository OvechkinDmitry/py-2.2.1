import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import math


def get_average_salary(row):
    """Возвращает среднее значение по зарплате из клонок DataFrame
    Args:
        row (Any): Строка из dataframe
    Returns:
        float: средняя зарплата
    """
    needed_curr = ['BYR', 'USD', 'EUR', 'KZT', 'UAH']
    salary_from, salary_to, salary_currency, salary = (row.salary_from, row.salary_to, row.salary_currency, row.salary)
    if type(salary_currency) is str:
        salary = (salary_from + salary_to) / 2 if not math.isnan(salary_from) and not math.isnan(salary_to) else\
        salary_from if not math.isnan(salary_from) else salary_to
        if salary_currency != 'RUR' and salary_currency in needed_curr:
            ratio_currency = cur.execute(
                f"""SELECT {salary_currency} FROM currencies 
                WHERE date='{f'{row.published_at[5:7]}-{row.published_at[:4]}'}'""").fetchone()[0]
            salary = float('NaN') if ratio_currency is None else salary * ratio_currency
        elif salary_currency != 'RUR':
            salary = float('NaN')
    return salary


cur = sqlite3.connect('av_salary.db').cursor()
engine = create_engine('sqlite:///av_salary.db')
pd.set_option('expand_frame_repr', False)
df = pd.read_csv('vacancies_dif_currencies.csv')
df.insert(1, 'salary', float('NaN'))
df['salary'] = df.apply(lambda row: get_average_salary(row), axis=1)
[df.pop(field) for field in ['salary_from', 'salary_to', 'salary_currency']]
df['published_at'] = df['published_at'].apply(lambda x: x[:10])
