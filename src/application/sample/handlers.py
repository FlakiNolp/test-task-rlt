from aiogram import Router, F
from aiogram.filters import CommandStart
import aiogram.types as aiogram_types
import json

from src.infrastructure.repositories.base import BaseRepository
from src.application.sample.filters import filter_dict
from src.domain.entities.insert_json import InsertJSON
from src.domain.values.iso_date import IsoDate
from src.domain.values.group_type import GroupType

router = Router()


@router.message(CommandStart())
async def start(message: aiogram_types.Message):
    await message.answer(f'Hi, {message.from_user.first_name}')


@router.message(F.text.func(filter_dict))
async def get_salaries(message: aiogram_types.Message, mongo: BaseRepository):
    try:
        dict_text = json.loads(message.text)
        insert_json = InsertJSON(dt_from=IsoDate(dict_text['dt_from']), dt_upto=IsoDate(dict_text['dt_upto']),
                                 group_type=GroupType(dict_text['group_type']))
        await message.answer(str((await mongo.get_aggregate_salaries(insert_json)).__dict__()).replace("""'""", '''"'''))

    except ValueError:
        await message.answer('Невалидный запос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": '
                             '"2022-12-31T23:59:00", "group_type": "month"}')


@router.message(~F.text.func(filter_dict))
async def get_salaries(message: aiogram_types.Message):
    await message.answer('Невалидный запос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": '
                         '"2022-12-31T23:59:00", "group_type": "month"}')
