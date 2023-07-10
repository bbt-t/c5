from asyncio import gather as asyncio_gather
from typing import LiteralString, Generator, Iterable
from urllib import request, error

from entity.hh import (
    HeadHunterAPIVacancies,
    HeadHunterVacancyEmployer,
    HeadHunterVacancySalary,
)

from aiohttp import ClientConnectorError
from aiohttp.client import ClientSession
from pydantic import BaseModel, AnyHttpUrl, NonNegativeInt, Field


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

    @property
    def default_currency(self):
        return self._default_currency

    @default_currency.setter
    def default_currency(self, currency: LiteralString):
        self._default_currency = currency

    async def set_currency_salary(self, session: ClientSession) -> None:
        """
        Async request. Currency exchange for the necessary.
        """
        url = f"https://open.er-api.com/v6/latest/{self.currency}"
        try:
            async with session.get(url) as response:
                data = await response.json()

            if data["result"] == "success":
                self.salary = data["rates"][self.default_currency] * self.salary
        except ClientConnectorError as e:
            print(f"Connection error -> {e}")
        except KeyError:
            print(f"! {self.currency} not supported !")


class HeadHunterAPI:
    """
    Class for working with API HeadHunter.
    """

    query_by_employers = "https://api.hh.ru/vacancies?employer_id={}&per_page={}"
    query_by_word = "https://api.hh.ru/vacancies?text={}&per_page={}"

    async def get_by_employers(self, employers: Iterable, amt: int):
        async with ClientSession() as session:
            results = [
                self._fetch(session, self.query_by_employers.format(emp_id, amt))
                for emp_id in employers
            ]
            data_raw = await asyncio_gather(*results)

        async with ClientSession() as session:
            for vac in (
                vacancy := [
                    Vacancy(
                        title=item.name,
                        url=item.alternate_url,
                        employer=item.employer,
                        salary=0 if not item.salary else self._get_salary(item.salary),
                        currency="RUB"
                        if not item.salary
                        else self._currency_mapping(item.salary.currency),
                    )
                    for item in sum(
                        [
                            HeadHunterAPIVacancies.parse_raw(data).items
                            for data in data_raw
                        ],
                        [],
                    )
                ]
            ):
                await vac.set_currency_salary(session)

        return vacancy

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
        """
        Sets the value of salary.
        """
        if salary.salary_minimal:
            return salary.salary_minimal
        return salary.salary_maximum

    @staticmethod
    async def _fetch(session: ClientSession, url: str):
        """
        Async request.
        """
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
