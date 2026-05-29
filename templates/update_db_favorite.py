import sqlite3

conn = sqlite3.connect("calendar.db")
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE events ADD COLUMN favorite INTEGER DEFAULT 0")
    print("Колонка favorite добавлена.")
except:
    print("Колонка уже существует.")
conn.commit()
conn.close()