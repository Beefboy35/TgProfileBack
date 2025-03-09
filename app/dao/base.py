

from typing import List, TypeVar, Generic, Type, Optional

from pydantic import BaseModel
from tortoise import Tortoise, fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from loguru import logger
from app.dao.models import Base

T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: Type[T] = None

    def init(self, session: Tortoise):
        self._session = session
        if self.model is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def find_one_or_none_by_id(self, data_id: int) -> Optional[T]:
        try:
            record = await self.model.get_or_none(id=data_id)
            log_message = f"Запись {self.model._meta.table} с ID {data_id} {'найдена' if record else 'не найдена'}."
            logger.info(log_message)
            return record
        except DoesNotExist:
            logger.error(f"Запись с ID {data_id} не найдена.")
            raise
        except Exception as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise

    async def add(self, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {self.model.__name__} с параметрами: {values_dict}")

        try:
            new_instance = await self.model.create(**values_dict)  # Создаем новую запись
            logger.info(f"Запись {self.model.__name__} успешно добавлена.")
            return new_instance
        except IntegrityError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise