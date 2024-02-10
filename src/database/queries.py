import datetime
import asyncio
import sqlite3
import aiosqlite
from constants import db_file, MetricType
from metric import Metric


async def db_add_metric(metric: Metric) -> False:
    try:
        async with aiosqlite.connect(db_file, check_same_thread=False) as connection:
            cursor = await connection.cursor()
            await cursor.execute(
                '''
                INSERT INTO Metrics (user_id, type, name, time) VALUES (?, ?, ?, ?)
                ''',
                (metric.user_id, metric.type.value, metric.name, str(metric.time))
            )
            await connection.commit()
    except Exception as e:
        print(repr(e))
        return False
    print(123)
    return True

# async def main():
#     m = Metric(123123123)
#     m.set_name('qwe')
#     m.set_time(datetime.time(23, 30))
#     m.set_type(MetricType.NON_NUMERIC)
#     await db_add_metric(m)
#     print(456)

# # if __name__ == '__main__':
# asyncio.run(main())
