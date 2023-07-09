from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, AnyUrl, Field, NonNegativeInt


class HeadHunterVacancyAddress(BaseModel):
    building: str | None
    city: str | None
    description: str | None
    id: str
    lat: float | None
    lng: float | None
    metro: dict | None
    metro_stations: list
    raw: str | None
    street: str | None


class HeadHunterVacancyArea(BaseModel):
    id: str
    name: str
    url: AnyUrl


class HeadHunterVacancyEmployer(BaseModel):
    accredited_it_employer: bool | None
    alternate_url: str | None
    id: str | None
    logo_urls: dict | None
    name: str
    trusted: bool
    url: AnyUrl | None
    vacancies_url: AnyUrl | None


class FieldIDName(BaseModel):
    id: str
    name: str


class HeadHunterVacancySalary(BaseModel):
    currency: Literal[
        "UZS", "USD", "UAH", "RUR", "KZT", "KGS", "GEL", "EUR", "BYR", "AZN"
    ]
    salary_minimal: Optional[NonNegativeInt] = Field(alias="from")
    gross: bool | None
    salary_maximum: Optional[NonNegativeInt] = Field(alias="to")


class HeadHunterVacancySnippet(BaseModel):
    requirement: str | None
    responsibility: str | None


class HeadHunterVacancyItem(BaseModel):
    accept_incomplete_resumes: bool
    accept_temporary: bool
    address: HeadHunterVacancyAddress | None
    adv_response_url: str | None
    alternate_url: AnyUrl
    apply_alternate_url: AnyUrl
    archived: bool
    area: HeadHunterVacancyArea
    contacts: None
    created_at: datetime
    department: dict | None
    employer: HeadHunterVacancyEmployer
    employment: FieldIDName
    experience: FieldIDName
    has_test: bool
    id: str
    insider_interview: dict | None
    name: str
    premium: bool
    professional_roles: list[FieldIDName]
    published_at: datetime
    relations: list
    response_letter_required: bool
    response_url: AnyUrl | None
    salary: HeadHunterVacancySalary | None
    schedule: None
    snippet: HeadHunterVacancySnippet
    sort_point_distance: None
    type: FieldIDName
    url: AnyUrl
    working_days: list
    working_time_intervals: list
    working_time_modes: list


class HeadHunterAPIVacancies(BaseModel):
    alternate_url: str
    arguments: None
    clusters: None
    found: int
    items: list[HeadHunterVacancyItem]
    page: int
    pages: int
    per_page: int
