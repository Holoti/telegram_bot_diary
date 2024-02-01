import sqlite3
import datetime

class DBThing:
    """
    So far used only for database communication, am not sure with the name of the class
    """
    def __init__(self):
        self.init_sql()
        self.create_users_table()
        self.create_user_settings_table()

    def init_sql(self):
        self.connection = sqlite3.connect("database.sqlite", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
            uid INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def create_user_settings_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS UserSettings (
            uid INTEGER PRIMARY KEY,
            evening_time TEXT,
            morning_time TEXT
            )
            """
        )
        self.connection.commit()

    def add_user(self, uid: int, username: str, first_name: str, last_name: str) -> bool:
        self.cursor.execute(f'SELECT EXISTS(SELECT 1 FROM Users WHERE uid={uid})')
        if self.cursor.fetchall()[0][0] == 1:
            return False

        self.cursor.execute(f'INSERT INTO Users (uid, username, first_name, last_name) VALUES ({uid}, "{username}", "{first_name}", "{last_name}")')
        self.cursor.execute(f'INSERT INTO UserSettings (uid) VALUES ("{uid}")')
        self.connection.commit()
        return True

    def set_user_setting(self, uid: int, evening_time: str = None, morning_time: str = None) -> bool:
        if evening_time is None and morning_time is None:
            print(f"No time given! uid={uid}")
            return False

        if evening_time:
            self.cursor.execute(f'UPDATE UserSettings SET evening_time="{evening_time}" WHERE uid={uid}')
        if morning_time:
            self.cursor.execute(f'UPDATE UserSettings SET morning_time="{morning_time}" WHERE uid={uid}')
        self.connection.commit()
        return True

    def get_user_setting(self, uid: int) -> tuple:
        result = self.cursor.execute(f'SELECT evening_time, morning_time FROM UserSettings WHERE uid = {uid}').fetchone()
        return result

    def forget_user(self, uid: int):
        self.cursor.execute(f'DELETE FROM Users WHERE uid={uid}')
        self.cursor.execute(f'DELETE FROM UserSettings WHERE uid={uid}')
        self.connection.commit()

