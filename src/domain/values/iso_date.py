from dataclasses import dataclass, field
import datetime
from typing import override

from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class IsoDate(BaseValueObject[str]):
    value: str = field(init=False, default="")

    @override
    def __init__(self, value: str):
        if not value.endswith('+00:00'):
            value += '+00:00'
        object.__setattr__(self, "value", value)

    def validate(self):
        if isinstance(self.value, str):
            if not datetime.datetime.fromisoformat(self.value):
                raise ValueError('Date must be in ISO format')

    def as_generic_type(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.value)