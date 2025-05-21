from flask import g
import sqlite3

from helpers.application import app


DATABASE = 'censoescolar.db'

def make_dicts(cursor, row):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}

def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()