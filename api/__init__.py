from typing import Annotated

from pydantic import BaseModel
from fastapi import APIRouter, Cookie

router = APIRouter()


class UserMessage(BaseModel):
    author: str
    message: str


data = [
        {
            "author": "Akulij",
            "message": "Hello1",
            }
    ]


@router.get("/user_messages", response_model=list[UserMessage])
# async def user_messages(bearer: Annotated[str | None, Cookie()]) -> list[UserMessage]:
async def user_messages() -> list[UserMessage]:
    # print(f"{bearer=}")
    return list(map(lambda m: UserMessage(**m), data))
    return []
