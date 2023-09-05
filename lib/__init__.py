import sqlite3

CONN = sqlite3.connect('db/development.db')
CURSOR = CONN.cursor()
