import asyncio
import sqlite3
from constants import db_file

async def init_db():
    with sqlite3.connect(db_file, check_same_thread=False) as connection:
        cursor = connection.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Metrics (
            metric_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type BLOB NOT NULL,
            name TEXT NOT NULL,
            time TEXT
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Data (
            data_id INTEGER PRIMARY KEY,
            metric_id INTEGER NOT NULL,
            number INTEGER,
            commentary TEXT,
            datetime TEXT NOT NULL,
            FOREIGN KEY (metric_id)
                REFERENCES Metrics (metric_id)
            )
            '''
        )
        connection.commit()


async def main():
    await init_db('src/database/db.sqlite')


if __name__ == '__main__':
    asyncio.run(main())

