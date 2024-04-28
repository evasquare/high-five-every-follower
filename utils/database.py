import sqlite3
from sqlite3 import Connection, Cursor
from _type_dicts import AtprotoUser


class DatabaseUtils:
    def __init__(self) -> None:
        self.create_tables()

    def create_tables(self) -> None:
        connection, cursor = self.get_connection()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS followers (
                did TEXT,
                display_name TEXT,
                handle TEXT
            )
            '''
        )
        self.commit_connection(connection)

    def find_user(self, did) -> AtprotoUser | None:
        _, cursor = self.get_connection()

        cursor.execute(
            '''
            SELECT *
            FROM followers
            WHERE did = ?
            ''',  (did,)
        )
        user = cursor.fetchone()
        if user is None:
            return None

        atproto_user: AtprotoUser = {
            "did": user[0],
            "display_name": user[1],
            "handle": user[2]
        }
        return atproto_user

    def insert_user(self, atproto_user: AtprotoUser) -> bool:
        if not atproto_user["did"] or not atproto_user["display_name"] or not atproto_user["handle"]:
            return False

        connection, cursor = self.get_connection()

        cursor.execute(
            '''
            INSERT INTO followers (
                did,
                display_name,
                handle
            )
            VALUES (?, ?, ?)
            ''',
            (
                atproto_user["did"],
                atproto_user["display_name"],
                atproto_user["handle"],
            )
        )

        return self.commit_connection(connection)

    def get_connection(self) -> tuple[Connection, Cursor]:
        connection = sqlite3.connect("./database/data.db")
        cursor = connection.cursor()
        return connection, cursor

    def commit_connection(self, connection: Connection) -> bool:
        try:
            connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            if connection:
                connection.close()
