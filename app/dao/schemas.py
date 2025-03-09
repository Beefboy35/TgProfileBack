from pydantic import BaseModel

class UserToAdd(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str | None
    nickname: str
