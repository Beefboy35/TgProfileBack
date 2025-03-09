from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from app.config import settings


def main_kb():
    kb_list = [[
    KeyboardButton(text="🤑Open app"),
    KeyboardButton(text="🧠About")
    ]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_key=True)
    return keyboard


def run_app(user_id: int):
    web_app = WebAppInfo(url=f"{settings.FRONT_URL}?telegramId={user_id}")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🤑Open app", web_app=web_app)]]
    )
    return keyboard