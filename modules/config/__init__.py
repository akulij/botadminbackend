from pydantic import (
    BaseModel,
    PostgresDsn,
)

# placeholder to emulate bot settings in backend
class Settings(BaseModel):
    database_uri: PostgresDsn
    qiwi_token: str
    bot_token: str
    support_chatid: int
    botname: str
