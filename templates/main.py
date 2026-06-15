from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os


app = FastAPI()

templates = Jinja2Templates(directory="/opt/render/project/src/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
