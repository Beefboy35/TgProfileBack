from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME COLUMN "time_to_birthday" TO "time_of_birthday";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME COLUMN "time_of_birthday" TO "time_to_birthday";"""
