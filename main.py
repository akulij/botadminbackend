from typing import Annotated
from fastapi import FastAPI, Form, Request

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

import api

app = FastAPI()

app.include_router(api.router, prefix="/api")

@app.get("/")
async def index(request: Request):
    return RedirectResponse("/index.html")

@app.post("/login")
async def login(login: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(f"{login=}, {password=}")
    return RedirectResponse("/statistics/index.html", status_code=303)

@app.get("/statistics/")
async def statistics():
    return RedirectResponse("/statistics/index.html")

@app.get("/chats/")
async def chats():
    return RedirectResponse("/chats/index.html")

app.mount("/", StaticFiles(directory="../botadmin/dist"), name="static")
