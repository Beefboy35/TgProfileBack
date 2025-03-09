
from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.dao.dao import UserDAO
from app.dao.models import User
from app.dao.schemas import UserToAdd

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/get_all")
async def get_all():
    try:
        users = await User.all()
        return users
    except Exception as e:
        logger.error(f"Ошибка при получение всех юзеров: {e}")

@router.post("/add_user")
async def add_user(user: UserToAdd):
    try:
        user = await User.create(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            nickname=user.nickname
        )
        return user
    except IntegrityError:
        # Обработка случая, если пользователь уже существует
        logger.info(f"Пользователь {user.first_name} уже существует")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Пользователь уже существует")
    except Exception as e:
        logger.error(f"Ошибка при добавление юзера: {e}")
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Что-то пошло не так попробуйте позже")

@router.post("/update_birthday/{telegram_id}")
async def update_birthday(telegram_id: int, date_of_birth: str):
    try:
        await User.filter(telegram_id=telegram_id).update(time_of_birthday=date_of_birth)
        return JSONResponse(status_code=200, content="Birthday updated successfully")
    except IntegrityError:
        return JSONResponse(status_code=404, content="User not found")
    except Exception as e:
        logger.error(f"Ошибка при добавлении даты рождения юзера: {e}")
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Что-то пошло не так попробуйте позже")
