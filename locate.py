import sqlite3

conn = sqlite3.connect("calendar.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE events ADD COLUMN location TEXT")

conn.commit()
conn.close()

print("Колонка location добавлена в базу данных.")