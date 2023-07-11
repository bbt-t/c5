# Choice the DB manager

from dataclasses import dataclass, field

from storage.headhunter import DBManagerHH
from storage.interface import DBManager


@dataclass(slots=True, eq=False)
class Storage:
    """
    Init DB manager by param.
    """

    db: DBManager = field(init=False)
    param: dict

    def __post_init__(self):
        self.db = DBManagerHH(**self.param)
