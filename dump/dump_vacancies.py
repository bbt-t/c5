from secrets import SystemRandom
from typing import Iterable

from dump.api import HeadHunterAPI
from storage.interface import Database
from storage.pg import PG
from tools import FileReader

from psycopg import DatabaseError


async def get_vacancies_by_employer(employers_id: Iterable, job_api: HeadHunterAPI) -> list:
    """
    Receives vacancies of random employers.
    :param employers_id:
    :param job_api:
    :return: vacancies
    """
    return await job_api.get_by_employers(employers_id, 100)


def get_employers(job_api: HeadHunterAPI) -> set:
    """
    Receives a list employers.
    :param job_api: api-obj
    :return: employers ids
    """
    employers_py = set(job_api.get_employers_id("python", 100))
    employers_go = set(job_api.get_employers_id("go", 100))

    return employers_py | employers_go


async def dump(database: Database, job_api: HeadHunterAPI, count: int = 20) -> None:
    """
    Receives a list employers -> list of vacancies of random employers -> write if to DB.
    :param database: db-object
    :param job_api: api-object
    :param count: how many employers
    """
    employers_ids = get_employers(job_api)
    if len(employers_ids) >= count:
        vacancies = await get_vacancies_by_employer(
            SystemRandom.sample(SystemRandom(), list(employers_ids), count),
            job_api,
        )
    else:
        vacancies = await get_vacancies_by_employer(
            employers_ids,
            job_api,
        )

    conn = database.conn()
    cursor = conn.cursor()

    try:
        for item in vacancies:
            cursor.execute(
                "INSERT INTO vacancies(title,company_name,salary,link) VALUES (%s,%s,%s,%s)",
                (item.title, item.employer.name, item.salary, item.url),
            )

        conn.commit()
    except DatabaseError as err:
        print("error in transaction -> ", err)

        conn.rollback()

        print("<- ROLLBACK <-", err)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("DB connection is closed")


async def init() -> None:
    """
    Initialized test data records a DB.
    """
    reader = FileReader("dump/queries.sql")
    db = PG()

    db.create_tables(reader)
    api = HeadHunterAPI()

    await dump(db, api)
