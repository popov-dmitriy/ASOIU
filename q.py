import sqlite3

con = sqlite3.connect("database.db")
link = con.cursor()

link.execute("SELECT name, category, price FROM game")
con.commit()
print(link.fetchall())
link.fetchall()
