import pandas as pd
import sqlite3

df = pd.read_csv('currencies.csv')
df.columns = df.columns.str.strip()
conn = sqlite3.connect('currencies.db')
df.to_sql('currencies', conn, index=False)