import sqlite3
import pandas as pd

#запрос средней зарплаты по годам
req_salary_by_year = """
        SELECT strftime('%Y', published_at) as year, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary
        FROM vacancies 
        GROUP BY strftime('%Y', published_at);
    """

#запрос кол-ва всех вакансий по годам
req_count_by_year = """
        SELECT strftime('%Y', published_at) as year, COUNT(*) as count
        FROM vacancies 
        GROUP BY strftime('%Y', published_at);
    """

# запрос по средней зарплате передаваемой профессии
req_salary_by_year_needed = lambda prof : f" \
        SELECT strftime('%Y', published_at) as year, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary \
        FROM vacancies \
        WHERE name LIKE '%{prof}%' \
        GROUP BY strftime('%Y', published_at); \
    "

# запрос количества пердаваемой профессии по годам
req_count_by_year_needed = lambda prof: f" \
        SELECT strftime('%Y', published_at) as year, COUNT(*) as count \
        FROM vacancies \
        WHERE name LIKE '%{prof}%' \
        GROUP BY strftime('%Y', published_at); \
    "

# запрос средней зарплаты
req_salary_by_area = """
       SELECT area_name, COUNT(*) as count, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary
       FROM vacancies 
       GROUP BY area_name 
       HAVING count > (SELECT COUNT(*) FROM vacancies) / 100
       ORDER BY avg_salary DESC
       LIMIT 10;
   """


# запрос доли городов
req_portion_of_area = """
        SELECT area_name, COUNT(*) as count, 
            CAST(ROUND(CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM vacancies) * 100, 4) AS VARCHAR) || '%' AS piece
        FROM vacancies 
        GROUP BY area_name 
        HAVING count > (SELECT COUNT(*) FROM vacancies) / 100
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """


def pass_request(connect, sql_request, console_message):
    """Делает запрос в бд и выводит результат в консоль"""
    print(console_message)
    print(pd.read_sql(sql_request, connect))
    print()


profession = "Аналитик"
connect = sqlite3.connect("vacancies.db")
pass_request(connect, req_salary_by_year, "Динамика уровня зарплат по годам")
pass_request(connect, req_count_by_year, "Динамика количества вакансий по годам")
pass_request(connect, req_salary_by_year_needed(profession), "Динамика уровня зарплат по годам для выбранной профессии")
pass_request(connect, req_count_by_year_needed(profession), "Динамика количества вакансий по годам для выбранной профессии")
pass_request(connect, req_salary_by_area, "Уровень зарплат по городам")
pass_request(connect, req_portion_of_area, "Доля вакансий по городам")
