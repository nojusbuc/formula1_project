import sqlite3

conn = sqlite3.connect('./local_database/pydatabase.db')
cur = conn.cursor()

# cur.execute(
#     '''CREATE TABLE runningProgram (id INTEGER PRIMARY KEY, shouldRun TEXT)''')
# cur.execute(
#     """INSERT INTO runningProgram (id, shouldRun) VALUES (0, 'False')""")
cur.execute('UPDATE runningProgram SET shouldRun = "True"')
conn.commit()

conn.close()
