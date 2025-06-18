import psycopg2

connection = psycopg2.connect(
    dbname='censoescolar',
    user='postgres',
    password='123456789',
    host='localhost',
    port='5434'
)

cursor = connection.cursor()

with open('schema.sql', 'r') as f:
    cursor.execute(f.read())

connection.commit()

cursor.close()
connection.close()
