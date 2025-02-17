import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute("INSERT INTO users (username,password) VALUES ('Mikolaj','Wafel')")

# query = """
#     SELECT date_time, username AS user, message, 'public' AS message_type
#     FROM logs
#     WHERE username NOT LIKE 'System'
#     UNION ALL
#     SELECT date_time, destination AS user, message, 'private' AS message_type
#     FROM logs_private
#     WHERE sender = ? OR destination = ?
#     ORDER BY date_time;
#     """
# cursor.execute(query,("Dawid","Dawid"))
# results = cursor.fetchall()
# for rows in results:
#      print(rows)
# cursor.execute("DELETE FROM logs;")
# cursor.execute("DELETE FROM logs_private;")
conn.commit()
conn.close()

