# DB models

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, eq=False)
class Count:
    round: int


@dataclass(slots=True, eq=False)
class RowID:
    id: UUID


@dataclass(slots=True, eq=False)
class CompanyAndVacanciesCount:
    company_name: str
    row_count: int


@dataclass(slots=True, eq=False)
class VacancyInfo:
    title: str
    company_name: str
    salary: tuple[int, int]
    link: str
