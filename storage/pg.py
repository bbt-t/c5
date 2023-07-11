# Database implementation

from os import getenv
from typing import Mapping

from psycopg import connect as psycopg3_connect
from psycopg import OperationalError

from config import DBConfigFile, DBConfigENV
from storage.interface import Reader


class PG:
    """
    Database.
    """

    def __init__(self, cfg: DBConfigENV | DBConfigFile):
        self.cfg = cfg

    def create_tables(self, reader: Reader):
        with self.conn() as conn:
            conn.cursor().execute(reader.read())

    def conn(self):
        """
        Connect to database.
        """
        try:
            connect = psycopg3_connect(
                host=self.cfg.host,
                port=self.cfg.port,
                dbname=self.cfg.db_name,
                user=self.cfg.db_user,
                password=self.cfg.password.get_secret_value(),
            )
        except OperationalError as err:
            print("Can't connect to DB -> ", err)
            raise SystemExit
        return connect
