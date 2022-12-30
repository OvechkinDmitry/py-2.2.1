import pandas as pd
from sqlalchemy import create_engine
import sqlite3

df = pd.read_csv('currencies.csv')
engine = create_engine('sqlite:///av_salary.db')
df.columns = df.columns.str.strip()
conn = sqlite3.connect('currencies.db')
df.to_sql('currencies', conn, index=False)