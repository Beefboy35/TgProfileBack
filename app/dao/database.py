from tortoise import Tortoise

from app.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": settings.DB_URL
    },
    "apps": {
        "models": {
            "models": ["app.dao.models", "aerich.models"],
            "default_connection": "default",
        }
    }
}
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()