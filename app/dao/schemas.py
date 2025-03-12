from pydantic import BaseModel

class UserToAdd(BaseModel):
    telegram_id: str
    first_name: str
    last_name: str | None
    nickname: str

class UserToReturn(UserToAdd):
    time_of_birthday: str
    age: int

class UpdateBirthdayRequest(BaseModel):
    telegram_id: str
    date_of_birth: str
    age: int

