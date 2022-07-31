import sqlite3

conn = sqlite3.connect('./f1_telem/local_database/test_db.db')
cur = conn.cursor()

# cur.execute(
#     '''CREATE TABLE runningProgram (id INTEGER PRIMARY KEY, shouldRun TEXT)''')
# cur.execute(
#     """INSERT INTO runningProgram (id, shouldRun) VALUES (0, 'False')""")
# cur.execute('UPDATE runningProgram SET shouldRun = "True"')

create_command = 'CREATE TABLE lap_data (id INTEGER PRIMARY KEY, lap_time FLOAT, sector1_time FLOAT, sector2_time FLOAT, sector3_time FLOAT, current_sector INTEGER, is_s1_best BOOL, is_s2_best BOOL, is_s3_best BOOL, is_lap_time_best BOOL, game_mode TEXT)'

cur.execute(create_command)
# print_command = 'SELECT * FROM lap_data'
# cur.execute('SELECT * FROM lap_data')
conn.commit()


# print(data)

conn.close()
