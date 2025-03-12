import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger

from app.bot.router import router
from app.config import settings

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'), BotCommand(command='open_app', description='Открыть приложение')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()
    dp.include_router(router)
    await bot.delete_webhook()


async def stop_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот остановлен")

