# Interfaces module

from typing import Protocol


class Reader(Protocol):
    def read(self) -> str:
        ...


class Database(Protocol):
    def create_tables(self, reader: Reader):
        ...

    def conn(self):
        ...


class DBManager(Protocol):
    def get_companies_and_vacancies_count(self) -> list:
        ...

    def get_all_vacancies(self) -> list:
        ...

    def get_avg_salary(self):
        ...

    def get_vacancies_with_higher_salary(self, search) -> list:
        ...
