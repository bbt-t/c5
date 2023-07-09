from asyncio import gather as asyncio_gather
from aiohttp.client import ClientSession

from entity.hh import (
    HeadHunterAPIVacancies,
    HeadHunterVacancyEmployer,
    HeadHunterVacancySalary,
)
from typing import LiteralString, Generator, Iterable
from urllib import request, error

from orjson import dumps, loads
from pydantic import BaseModel, AnyHttpUrl, NonNegativeInt, Field


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return dumps(v, default=default).decode()


class Vacancy(BaseModel):
    """
    Class Vacancy
    """

    title: str
    employer: HeadHunterVacancyEmployer
    url: AnyHttpUrl | None
    salary: NonNegativeInt = Field(default=0)
    currency: str = "RUB"
    _default_currency: str = "RUB"

    class Config:
        """
        Fast serialize.
        """

        json_loads = loads
        json_dumps = orjson_dumps

    @property
    def default_currency(self):
        return self._default_currency

    @default_currency.setter
    def default_currency(self, currency: LiteralString):
        self._default_currency = currency

    def currency_exchange_salary(self) -> int | None:
        try:
            with request.urlopen(
                f"https://open.er-api.com/v6/latest/{self.currency}"
            ) as url:
                data = loads(url.read().decode())

            if data["result"] == "success":
                return data["rates"][self.default_currency] * self.salary
        except error:
            print(f"! {self.currency} not supported !")
        except KeyError as e:
            print(f"error :: {repr(e)} ::")


class HeadHunterAPI:
    """
    Class for working with API HeadHunter.
    """

    query_by_employers = "https://api.hh.ru/vacancies?employer_id={}&per_page={}"
    query_by_word = "https://api.hh.ru/vacancies?text={}&per_page={}"

    async def get_by_employers(self, employers: Iterable, amt: int):
        async with ClientSession() as session:
            results = [
                self.fetch(session, self.query_by_employers.format(emp_id, amt))
                for emp_id in employers
            ]
            data_raw = await asyncio_gather(*results)

        vacancies_items = [
            HeadHunterAPIVacancies.parse_raw(data).items for data in data_raw
        ]
        return [
            Vacancy(
                title=item.name,
                url=item.alternate_url,
                employer=item.employer,
                salary=0 if not item.salary else self._get_salary(item.salary),
                currency="RUB"
                if not item.salary
                else self._currency_mapping(item.salary.currency),
            )
            for item in sum(vacancies_items, [])
        ]

    def get_employers_id(self, search: str, amt: int | str) -> Generator:
        """
        Search query.
        :param amt: how much to get (no more than 100)
        :param search: what we want to find
        :return: received vacancies containing the word (search param) in Vacancy-object
        """
        data_raw: str = self._load_from_url(self.query_by_word.format(search, amt))

        return (
            item.employer.id
            for item in HeadHunterAPIVacancies.parse_raw(data_raw).items
        )

    @staticmethod
    def _get_salary(salary: HeadHunterVacancySalary):
        if salary.salary_minimal:
            return salary.salary_minimal
        return salary.salary_maximum

    @staticmethod
    async def fetch(session: ClientSession, url: str):
        async with session.get(url) as response:
            return await response.text()

    @staticmethod
    def _load_from_url(url: str) -> str | None:
        """
        Load json (from url).
        :param url: URL to upload data
        :return: loaded data from url
        """
        try:
            with request.urlopen(url) as url:
                return url.read().decode()
        except error as e:
            print(f"error :: {repr(e)} ::")

    @staticmethod
    def _currency_mapping(currency: str) -> str | None:
        """
        Mapping currency names.
        param currency: currency abbreviation
        return: correct name
        """
        currency_map: dict = {
            "RUR": "RUB",
            "BYR": "BYN",
            "UAH": "UAH",
            "USD": "USD",
            "EUR": "EUR",
            "KZT": "KZT",
            "UZS": "UZS",
            "KGS": "KGS",
            "AZN": "AZN",
            "GEL": "GEL",
        }
        return currency_map.get(currency)
