import sqlite3

conn = sqlite3.connect("calendar.db")
cursor = conn.cursor()
cursor.execute("ALTER TABLE events ADD COLUMN notify INTEGER DEFAULT 0")
conn.commit()
conn.close()
print("Колонка notify добавлена.")