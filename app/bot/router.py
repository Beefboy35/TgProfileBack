import asyncio

import aiohttp
from aiogram import Router, F, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram.filters import Command
from loguru import logger
from starlette import status
from tortoise import Tortoise
from tortoise.exceptions import IntegrityError

from app.bot.kbs import run_app, main_kb
from app.config import settings
from app.dao.database import init_db
from app.dao.models import User


router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(f"Рады тебя видеть, {msg.from_user.full_name}! Нажимай скорее на кнопку и запускай приложение!", reply_markup=main_kb())

@router.message(F.text == "🧠About")
async def get_info(msg: Message):
    await msg.answer("Данное приложение создано в качестве прототипа на стеке: Vue3, TypeScript, Ta FastAPI, Postgresql, Tortoise ORM")

@router.message(F.text == "🤑Open app")
@router.message(Command("open_app"))
async def open_app(msg: Message):
    telegram_id = int(msg.from_user.id)
    username = msg.from_user.full_name
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name

    # Создаем объект User
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        nickname=username
    )
    try:
        # Сохраняем пользователя в базу данных
        await user.save()
        logger.info(f"Пользователь {username}  добавлен в бд")
        await msg.answer("Launch app!🚀", reply_markup=run_app(telegram_id))
    except IntegrityError:
        # Обработка случая, если пользователь уже существует
        logger.info(f"Пользователь {username} уже существует")
        await msg.answer("Launch app!🚀", reply_markup=run_app(telegram_id))

    except Exception as e:
        await msg.answer("Something went wrong. Try again later.")
        logger.error(f"Unexpected error: {e}")
        raise e


