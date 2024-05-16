from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.insert_json import InsertJSON
from src.domain.entities.out_json import OutputJSON


@dataclass
class BaseRepository(ABC):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BaseRepository, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    async def get_aggregate_salaries(self, insert_json: InsertJSON) -> OutputJSON:
        ...
