from typing import Optional, AsyncIterator
import datetime

from sqlmodel import Column, SQLModel, Field, select, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import BigInteger, sql, table

from config import Settings


class UserV1(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column(BigInteger(), primary_key=True))
    name: str
    nickname: Optional[str]
    state: str = Field(default="start")
    is_admin: bool = Field(default=False)
    last_activity: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# class FAQ(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     question: str
#     answer: str
#     category: str

class BotInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column(BigInteger(), primary_key=True))
    name: str
    nickname: str = Field(unique=True)
    version: int

class BotOwner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column(BigInteger(), primary_key=True))
    login: str
    password: str
    botname: str = Field(unique=True)

class ActionV1(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column(BigInteger(), primary_key=True))
    bot: str
    username: Optional[str]
    userid: int
    actiontype: str
    actionjson: str
    time: datetime.datetime


class DB:
    def __init__(self, config: Settings):
        self.engine = create_async_engine(config.database_uri)

    async def get_user_byid(self, id: int) -> UserV1 | None:
        async with AsyncSession(self.engine) as session:
            user = await session.get(UserV1, id)

        return user

    async def create_user(self, user: UserV1):
        async with AsyncSession(self.engine) as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

    async def set_user_state(self, user: UserV1, state: str):
        user.state = state
        async with AsyncSession(self.engine) as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

    async def get_all_user_ids(self) -> list[int]:
        async with AsyncSession(self.engine) as session:
            q = select(UserV1)
            e = await session.exec(q)
            users = e.all()

        return list(map(lambda u: u.id, users))
