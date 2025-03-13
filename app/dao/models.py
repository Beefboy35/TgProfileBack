


import uuid
from datetime import datetime
from decimal import Decimal

from tortoise import  fields, Model



class Base(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    class Meta:
        abstract = True


class User(Base):
    """
    Модель пользователя.
    Поля:
        telegram_id (int): Уникальный идентификатор пользователя в Telegram.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        nickname (str): Никнейм пользователя.
        age (int): Возраст пользователя.
        time_of_birthday (Optional[str]): Время до дня рождения (может быть None).
    """
    telegram_id = fields.CharField(max_length=10, unique=True)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64, null=True)
    nickname = fields.CharField(max_length=64)
    age = fields.IntField(null=True)
    time_of_birthday = fields.CharField(null=True, max_length=64)

    class Meta:
        table = "users"