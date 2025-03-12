
from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


from app.dao.models import User
from app.dao.schemas import UserToAdd, UpdateBirthdayRequest, UserToReturn

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/get_all")
async def get_all():
    try:
        users = await User.all()
        return users
    except Exception as e:
        logger.error(f"Ошибка при получение всех юзеров: {e}")

@router.get("/get_by_id/{telegram_id}")
async def get_user_by_tg_id(telegram_id: int):
    user = await User.get_or_none(telegram_id=telegram_id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
    return UserToReturn(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        last_name=user.last_name,
        nickname=user.nickname,
        time_of_birthday=user.time_of_birthday,
        age=user.age
    )
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

@router.post("/update_birthday")
async def update_birthday(request: UpdateBirthdayRequest):
    try:
        await User.filter(telegram_id=request.telegram_id).update(time_of_birthday=request.date_of_birth, age=request.age)
        return JSONResponse(status_code=200, content="Дата рождения успешно добавлена!")
    except IntegrityError:
        return JSONResponse(status_code=404, content="User not found")
    except Exception as e:
        logger.error(f"Ошибка при добавлении даты рождения юзера: {e}")
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=f"Что-то пошло не так попробуйте позже: {str(e)}")
