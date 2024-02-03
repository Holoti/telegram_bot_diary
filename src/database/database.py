from sqlalchemy.ext.asyncio import (
    create_async_engine
)
from sqlalchemy import (
    text
)
import asyncio

db_path = 'src/database/database.sqlite'
async_engine = create_async_engine(
    url=f'sqlite+aiosqlite:///{db_path}?check_same_thread=False',
    echo=False
)

async def add_user(uid: int, username: str, first_name: str, last_name: str):
    async with async_engine.connect() as connection:
        await connection.execute(text(f'INSERT INTO Users (uid, username, first_name, last_name) VALUES ({uid}, "{username}", "{first_name}", "{last_name}")'))
        await connection.execute(text(f'INSERT INTO UserSettings (uid) VALUES ("{uid}")'))
        await connection.commit()

asyncio.run(add_user(1, "dummy_name", "Dummy", "Danny"))
