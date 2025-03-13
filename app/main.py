from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn
from aiogram.types import Update
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from tortoise import Tortoise
from app.api.router import router as api_router
from app.bot.create_bot import start_bot, stop_bot, dp, bot
from app.config import settings
from app.dao.database import init_db

webhook_url = settings.BASE_URL + "/webhook"

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    await init_db()
    await bot.set_webhook(
         url=webhook_url,
         allowed_updates=dp.resolve_used_update_types(),
         drop_pending_updates=True
    )
    logger.success(f"Вебхук установлен: {webhook_url}")
    await start_bot()
    yield
    await stop_bot()
    await Tortoise.close_connections()
    logger.info("Завершение работы приложения...")

def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   Returns:
       Сконфигурированное приложение FastAPI
   """
    app = FastAPI(
        title="TgAppProfile",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(api_router)
    return app
app = create_app()
@app.post("/webhook", summary="Эндпоинт используемый для передачи обновлений от бота")
async def webhook(request: Request) -> None:
    try:
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        logger.info("Обновление успешно обработано.")
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления с вебхука: {e}")
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="localhost", port=8005, reload=True)