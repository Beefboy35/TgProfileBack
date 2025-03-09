from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "time_to_birthday" TYPE VARCHAR(64) USING "time_to_birthday"::VARCHAR(64);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "time_to_birthday" TYPE TIMETZ USING "time_to_birthday"::TIMETZ;"""
