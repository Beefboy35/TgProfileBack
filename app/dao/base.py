

from typing import List, TypeVar, Generic, Type, Optional

from pydantic import BaseModel
from tortoise import Tortoise, fields
from tortoise.exceptions import DoesNotExist, IntegrityError
from loguru import logger
from app.dao.models import Base

T = TypeVar("T", bound=Base)

