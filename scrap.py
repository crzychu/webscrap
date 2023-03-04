import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

conn = sqlite3.connect('test_database.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS products (name text, price number, kcal number)')
conn.commit()

page = requests.get('https://zanimzbudujesz.pl/cennik-mcdonald/').text

soup = BeautifulSoup(page, 'lxml')
table = soup.find('figure', class_ = 'wp-block-table')

headers = ['name', 'price', 'kcal']

df = pd.DataFrame(columns = headers)

for row in table.find_all('tr')[1:]:
    data = row.find_all('td')
    row_data = [td.text.strip() for td in data]
    length = len(df)
    df.loc[length] = row_data

df['kcal'] = df['kcal'].str.extract('(\d+)', expand=False)
df['kcal'] = df['kcal'].astype(int)
df["price"] = df["price"].str.replace(',','.')
df["price"] = df["price"].str.replace('zł','')
df["price"] = df["price"].astype(float)
df["name"] = df["name"].str.replace('\ufeff', '')

df.to_sql('products', conn, if_exists='replace', index = False)


print(df.values)