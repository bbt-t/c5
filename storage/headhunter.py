# HeadHunter DB manager

from psycopg import DatabaseError
from psycopg.rows import class_row

from entity.database import VacancyInfo, RowID, Count, CompanyAndVacanciesCount
from storage.interface import Database


class DBManagerHH:
    """
    Implements an interface DBManager.
    """

    select_vacancies_info: str = (
        "SELECT title, company_name, salary, link FROM vacancies"
    )
    select_vacancy_by_word: str = (
        "SELECT id FROM vacancies WHERE LOWER(title) like LOWER('%{}%')"
    )
    select_avg_salary: str = (
        "SELECT ROUND(AVG(salary)) FROM vacancies WHERE salary != 0"
    )
    select_vacancy_count: str = "SELECT company_name, COUNT(*) AS row_count FROM vacancies GROUP BY company_name"

    def __init__(self, db_connect: Database) -> None:
        self.db_connect = db_connect

    def _execute(self, query, schema) -> list:
        """
        Query to db.
        :param query: request
        :param schema: class for collecting the result
        :return: result in list
        """
        conn = self.db_connect.conn()
        conn.read_only = True

        cursor = conn.cursor(row_factory=class_row(schema))
        try:
            cursor.execute(query)
            print("-> DONE!")
            return cursor.fetchall()
        except DatabaseError as err:
            print("error -> ", err)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("DB connection is closed")

    def get_companies_and_vacancies_count(self) -> list:
        """
        Gets a list of all companies and the number of vacancies for each company.
        """
        result = self._execute(self.select_vacancy_count, CompanyAndVacanciesCount)
        return result

    def get_all_vacancies(self) -> list:
        """
        Gets a list of all vacancies with the name of the company,
        job titles and salaries and links to the job.
        """
        result = self._execute(self.select_vacancies_info, VacancyInfo)
        return result

    def get_avg_salary(self):
        """
        Receives an average salary for vacancies.
        """
        result = self._execute(self.select_avg_salary, Count)
        return result

    def get_vacancies_with_higher_salary(self, search) -> list:
        """
        Gets a list of all vacancies,
        the names of which contain the words passed to the method, e.g "python".
        """
        result = self._execute(self.select_vacancy_by_word.format(search), RowID)
        return result
