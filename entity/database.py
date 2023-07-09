from dataclasses import dataclass
from uuid import UUID


@dataclass
class Count:
    round: int


@dataclass
class RowID:
    id: UUID


@dataclass
class CompanyAndVacanciesCount:
    company_name: str
    row_count: int


@dataclass
class VacancyInfo:
    title: str
    company_name: str
    salary: tuple[int, int]
    link: str
