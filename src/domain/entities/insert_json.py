import datetime
from dataclasses import dataclass
from typing import Literal

from src.domain.values.iso_date import IsoDate
from src.domain.values.group_type import GroupType


@dataclass
class InsertJSON:
    dt_from: IsoDate
    dt_upto: IsoDate
    group_type: GroupType

    @classmethod
    def create(cls, dt_from: IsoDate, dt_upto: IsoDate, group_type: GroupType) -> 'InsertJSON':
        return cls(dt_from, dt_upto, group_type)
