import sqlite3

conn = sqlite3.connect("calendar.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE events ADD COLUMN link TEXT")
except:
    pass

events = [
    ("Торжественные мероприятия, посвященные принятию военной присяги обучающимися ВУЦ", "2026-06-08", "2026-06-08", "Полигон ТВВИКУ", "https://www.utmn.ru/vuts/novosti/1299281/"),
    ("UTMN STAR — Отчётный фестиваль творческих объединений", "2026-06-06T18:00", "2026-06-06T23:59", "Концертный зал ТюмГУ", "https://vk.com/wall-142012747_23065"),
    ("Выставка исторической памяти, посвященная 9 мая", "2026-05-06", "2026-06-06", "Главный корпус, ул. Республики 9", "https://www.utmn.ru/news/stories/obshchestvo-i-kultura/1288380/"),
]

cursor.executemany("""
    INSERT INTO events (title, start_time, end_time, location, link)
    VALUES (?, ?, ?, ?, ?)
""", events)

conn.commit()
conn.close()

print("Добавлено мероприятия со ссылками.")