from asyncio import run

from config import PGConfig
from dump.dump_vacancies import init
from storage.db import Storage
from storage.pg import PG
from tools import FileReader


def main() -> None:
    """
    Main func.
    """
    reader = FileReader("dump/queries.sql")

    pg = PG(PGConfig().env)
    pg.create_tables(reader)

    param = {
        "db_connect": pg,
    }
    manager = Storage(param)

    print(manager.db.get_all_vacancies())
    print(manager.db.get_avg_salary())
    print(manager.db.get_companies_and_vacancies_count())
    print(manager.db.get_vacancies_with_higher_salary("python"))


if __name__ == "__main__":
    # for test:
    run(init("env"))  # dump to db
    main()  # test methods
