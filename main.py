from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

DB_NAME = "calendar.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            location TEXT,
            notify INTEGER DEFAULT 0,
            favorite INTEGER DEFAULT 0
        )
    """)
    try:
        cursor.execute("ALTER TABLE events ADD COLUMN favorite INTEGER DEFAULT 0")
    except:
        pass
    conn.commit()
    conn.close()


init_db()


class Event(BaseModel):
    title: str
    start: str
    end: str | None = None
    location: str | None = None
    notify: int = 0
    favorite: int = 0


class FavoriteUpdate(BaseModel):
    title: str
    start: str
    favorite: int


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/events")
def get_events():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, start_time, end_time, location, notify, favorite FROM events")
    rows = cursor.fetchall()
    conn.close()

    events_list = []
    for row in rows:
        events_list.append({
            "title": row[0],
            "start": row[1],
            "end": row[2],
            "location": row[3],
            "notify": row[4],
            "favorite": row[5]
        })
    return events_list


@app.get("/api/events/favorites")
def get_favorite_events():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, start_time, end_time, location, notify, favorite FROM events WHERE favorite = 1")
    rows = cursor.fetchall()
    conn.close()

    events_list = []
    for row in rows:
        events_list.append({
            "title": row[0],
            "start": row[1],
            "end": row[2],
            "location": row[3],
            "notify": row[4],
            "favorite": row[5]
        })
    return events_list


@app.post("/api/events")
def create_event(event: Event):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (title, start_time, end_time, location, notify, favorite) VALUES (?, ?, ?, ?, ?, ?)",
        (event.title, event.start, event.end, event.location, event.notify, event.favorite)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.put("/api/events/favorite")
def toggle_favorite(data: FavoriteUpdate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE events SET favorite = ? WHERE title = ? AND start_time = ?",
        (data.favorite, data.title, data.start)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.delete("/api/events/{title}")
def delete_event(title: str, start: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM events WHERE title = ? AND start_time = ?",
        (title, start)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"status": "ok"}


@app.get("/list", response_class=HTMLResponse)
def events_list(request: Request):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, start_time, end_time, location, notify, favorite FROM events ORDER BY start_time")
    rows = cursor.fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Список мероприятий</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h1>Список мероприятий</h1>
        <table>
            <tr><th>Название</th><th>Начало</th><th>Место</th><th>Избранное</th><th>Уведомление</th></tr>
    """
    for row in rows:
        fav_text = "Да" if row[5] else "Нет"
        notif_text = "Да" if row[4] else "Нет"
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[3] or ''}</td><td>{fav_text}</td><td>{notif_text}</td></tr>"
    html += "</table><br><a href='/'>Назад</a></body></html>"
    return html