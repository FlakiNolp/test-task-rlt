from dataclasses import dataclass

from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class GroupType(BaseValueObject[str]):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise ValueError(f'{self.value} is not a string')
        if self.value not in ['hour', 'day', 'month']:
            raise ValueError("group_type must be 'hour', 'day', 'month'")

    def as_generic_type(self) -> str:
        return self.value
