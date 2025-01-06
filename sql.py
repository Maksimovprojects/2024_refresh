import psycopg2 as pg2

password = 'Resiver28'

conn = pg2.connect(database='dvdrental', user='postgres', password=password, port = 5433, host = 'localhost')

cur = conn.cursor()
cur.execute("SELECT first_name FROM actor")
print(type(cur.fetchall()))

print(cur.fetchmany(10))
conn.close()
