from typing import Annotated

from pydantic import BaseModel
from fastapi import APIRouter, Cookie, HTTPException, status

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio.result import AsyncCommon

from db import DB
from config import config

router = APIRouter()

db = DB(config)


class UserMessage(BaseModel):
    author: str
    message: str
    userid: int


data = [
        {
            "author": "Akulij",
            "message": "Hello1",
            "userid": 123,
            }
    ]


def get_botname(token: str) -> str:
    wrong_token = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token"
            )
    try:
        data = jwt.decode(token, config.secret_key, algorithms=config.enc_algo)
    except JWTError:
        raise wrong_token

    botname: str = data["botname"]

    return botname


@router.get("/user_previews", response_model=list[UserMessage])
async def user_previews(token: Annotated[str, Cookie()], limit: int = 50) -> list[UserMessage]:
    botname: str = get_botname(token)
    # print(f"{bearer=}")
    messages = await db.get_user_previews(botname, limit=limit)
    return list(map(lambda m: UserMessage(**m), messages))
    return []

@router.get("/user_name")
async def user_name(userid: int):
    user = await db.get_user_byid(userid)

    if user:
        return {"name": user.name}
    else:
        return {"name": "none"}

@router.get("/user_messages")
async def user_messages(token: Annotated[str, Cookie()], userid: int, limit: int = 50):
    botname: str = get_botname(token)
    messages = await db.get_user_messages(userid, botname, limit=limit)
    # 2019-01-15T00:00:00.000
    gt = lambda a: a.time.strftime("%Y-%m-%dT%H:%M:%S")

    return list(map(lambda a: {"text": a.actionjson["message"], "date": gt(a)}, messages))

class SendMsgInfo(BaseModel):
    userid: int
    message: str

@router.post("/send_message")
async def send_message(token: Annotated[str, Cookie()], info: SendMsgInfo):
    botname = get_botname(token)

    await db.create_task_message(info.userid, botname, info.message)

    return "Successful!"

@router.get("/statistics")
async def get_statistics(token: Annotated[str, Cookie()]):
    botname = get_botname(token)

    ...

    return {
            "new_users": await db.get_new_users_per_day(botname),
            "total_users": await db.get_new_users_total(botname),
            "active_users_day": await db.get_active_users_per_day(botname),
            "active_users_24h": await db.get_active_users_per_hours(botname)
            }
