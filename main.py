from typing import Annotated
from fastapi import FastAPI, Form, Request, responses

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, errors

from jose import jwt, JWTError

import api

from db import DB
from config import config

app = FastAPI()

db = DB(config)

app.include_router(api.router, prefix="/api")

@app.get("/")
async def index(request: Request):
    return RedirectResponse("/index.html")

@app.post("/login")
async def login(login: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(f"{login=}, {password=}")
    is_correct = await db.check_password(login, password)
    if not is_correct: return RedirectResponse("/")

    token = jwt.encode({"botname": login}, config.secret_key, algorithm=config.enc_algo)

    response = RedirectResponse("/statistics/index.html", status_code=303)
    response.set_cookie("token", token)

    return response

@app.get("/admin/add_owner")
async def add_owner(login: str, password: str, botname: str, admin_password: str):
    if admin_password == config.secret_key:
        await db.add_owner(login, password, botname)

        return "Successful!"

@app.get("/statistics/")
async def statistics():
    return RedirectResponse("/statistics/index.html")

@app.get("/chats/")
async def chats():
    return RedirectResponse("/chats/index.html")

@app.get("/exit/")
async def unlogin():
    response = RedirectResponse("/")
    response.delete_cookie("token")
    
    return response

app.mount("/", StaticFiles(directory="../botadmin/dist"), name="static")
