# Database implementation

from os import getenv
from typing import Mapping

from psycopg import connect as psycopg3_connect
from psycopg import OperationalError

from storage.interface import Reader


class PG:
    """
    Database.
    """

    @staticmethod
    def _get_env() -> Mapping[str, str]:
        """
        Get values from envs.
        """
        return {
            "host": getenv("HOST", "localhost"),
            "port": getenv("PG_PORT", 5432),
            "dbname": getenv("POSTGRES_DB"),
            "user": getenv("POSTGRES_USER"),
            "password": getenv("POSTGRES_PASSWORD"),
        }

    def create_tables(self, reader: Reader):
        with self.conn() as conn:
            conn.cursor().execute(reader.read())

    def conn(self):
        """
        Connect to database.
        """
        try:
            connect = psycopg3_connect(**self._get_env())
        except OperationalError as err:
            print("Can't connect to DB -> ", err)
            raise SystemExit
        return connect
