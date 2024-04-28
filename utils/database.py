import sqlite3
from sqlite3 import Connection, Cursor
from _type_dicts import AtprotoUser


class DatabaseUtils:
    def __init__(self) -> None:
        self.create_tables()

    def create_tables(self) -> None:
        connection, cursor = self.get_connection()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS followers(did TEXT, display_name TEXT, handle TEXT, post_cid TEXT)"
        )
        self.commit_connection(connection)

    def find_follower(self, did) -> AtprotoUser | None:
        _, cursor = self.get_connection()

        cursor.execute(
            '''
            SELECT * FROM followers
            WHERE did = ?
            ''', (did,)
        )
        user = cursor.fetchone()
        if user is None:
            return None

        atproto_user: AtprotoUser = {
            "did": user[0],
            "display_name": user[1],
            "handle": user[2],
            "post_cid": user[3]
        }
        return atproto_user

    def insert_follower(self, atproto_user: AtprotoUser) -> bool:
        connection, cursor = self.get_connection()

        cursor.execute(
            '''
            INSERT INTO followers (did, display_name, handle, post_cid)
            VALUES (?, ?, ?, ?)
            ''',
            (
                atproto_user["did"],
                atproto_user["display_name"],
                atproto_user["handle"],
                atproto_user["post_cid"]
            )
        )

        return self.commit_connection(connection)

    def update_follower(self, atproto_user: AtprotoUser) -> bool:
        connection, cursor = self.get_connection()

        cursor.execute(
            '''
            UPDATE followers
            SET display_name = ?, handle = ?, post_cid = ?
            WHERE did = ?
            ''',
            (
                atproto_user["did"],
                atproto_user["display_name"],
                atproto_user["handle"],
                atproto_user["post_cid"]
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
