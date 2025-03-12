from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "telegram_id" VARCHAR(10) NOT NULL UNIQUE,
    "first_name" VARCHAR(64) NOT NULL,
    "last_name" VARCHAR(64),
    "nickname" VARCHAR(64) NOT NULL,
    "age" INT,
    "time_of_birthday" VARCHAR(64)
);
COMMENT ON TABLE "users" IS 'Модель пользователя.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
