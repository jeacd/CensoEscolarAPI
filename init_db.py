import sqlite3

connection = sqlite3.connect('censoescolar.db')

connection.execute("PRAGMA foreign_keys = ON;")

with open('schema.sql') as f:
    connection.executescript(f.read())
    
connection.commit()

connection.close()
