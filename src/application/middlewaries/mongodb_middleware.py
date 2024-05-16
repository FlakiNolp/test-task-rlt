from typing import Callable, Dict, Any, Awaitable
from aiogram.types.update import Update
from aiogram import BaseMiddleware

from src.infrastructure.repositories.mongo_repository import MongoRepository
from src.infrastructure.repositories.base import BaseRepository
from src.settings.config import config

mongodb: BaseRepository = MongoRepository(config.ME_CONFIG_MONGODB_SERVER, config.MONGO_INITDB_ROOT_USERNAME, config.MONGO_INITDB_ROOT_PASSWORD)


class MongoMiddleware(BaseMiddleware):
    def __init__(self):
        self.mongo = mongodb

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        data['mongo'] = self.mongo
        return await handler(event, data)
