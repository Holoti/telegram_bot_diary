import asyncio
import sqlite3
from constants import (
    db_file,
    MetricType
)
db_file = 'src/database/db.sqlite'
import datetime


class Metric:
    def __init__(self, user_id: int):
        self.user_id: int = user_id
        self.type: MetricType
        self.name: str
        self.time: datetime.time
    
    def set_type(self, type: MetricType):
        self.type = type
    
    def set_name(self, name: str):
        self.name = name
    
    def set_time(self, time: datetime.time):
        self.time = time

# m = Metric(1)
# m.set_type(MetricType.NON_NUMERIC)
# print(type(m.type))
# print(m.type)

# class Metric:
#     def __init__(self, user_id: int):
#         self.metric_id: int
#         with sqlite3.connect(db_file, check_same_thread=False) as connection:
#             cursor = connection.cursor()
#             cursor.execute(
#                 '''
#                 INSERT INTO Metrics (user_id) VALUES (?)
#                 ''',
#                 (user_id, )
#             )
#             print(cursor)

#     @property
#     async def name(self):
#         async with sqlite3.connect(db_file, check_same_thread=False) as connection:
#             cursor = await connection.cursor()
#             return await cursor.execute(
#                 '''
#                 SELECT * FROM Metrics WHERE metric_id = ?
#                 ''',
#                 (self.metric_id, )
#             ).fetchone()

# async def main():
#     m = await Metric(1)


# if __name__ == '__main__':
#     asyncio.run(main())