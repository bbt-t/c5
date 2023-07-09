from dataclasses import dataclass, field

from .headhunter import DBManagerHH
from .interface import DBManager


@dataclass(slots=True, eq=False)
class Storage:
    db: DBManager = field(init=False)
    param: dict

    def __post_init__(self):
        self.db = DBManagerHH(**self.param)
