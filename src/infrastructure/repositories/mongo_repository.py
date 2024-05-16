import datetime
from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient

from src.infrastructure.repositories.base import BaseRepository
from src.domain.entities.insert_json import InsertJSON
from src.domain.entities.out_json import OutputJSON


@dataclass
class MongoRepository(BaseRepository):
    mongo_host: str
    mongo_user: str
    mongo_password: str

    def __post_init__(self):
        self.__motor = AsyncIOMotorClient(host=self.mongo_host, port=27017, username=self.mongo_user, password=self.mongo_password, uuidRepresentation='standard')

    def get_collection(self):
        return self.__motor.get_database('sampleDB').get_collection('sample_collection')

    async def get_aggregate_salaries(self, insert_json: InsertJSON) -> OutputJSON:
        # Запрос в mongodb
        collection = self.get_collection()
        group_format: str
        if insert_json.group_type.as_generic_type() == 'hour':
            group_format = "%Y-%m-%dT%H:00:00+00:00"
        elif insert_json.group_type.as_generic_type() == 'day':
            group_format = "%Y-%m-%dT00:00:00+00:00"
        elif insert_json.group_type.as_generic_type() == 'month':
            group_format = "%Y-%m-01T00:00:00+00:00"

        pipeline = [
            {"$match": {"dt": {"$gte": insert_json.dt_from.as_generic_type(), "$lte": insert_json.dt_upto.as_generic_type()}}},
            {"$group": {
                "_id": {"$dateToString": {"format": group_format, "date": "$dt"}},
                "total": {"$sum": "$value"}
            }},
            {"$sort": {"_id": 1}}
        ]

        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)

        aggregated_data = [(datetime.datetime.fromisoformat(res['_id']), res['total']) for res in results]

        current = insert_json.dt_from.as_generic_type()
        labels = []

        # Формирование labels
        if insert_json.group_type.as_generic_type() == 'hour':
            while current <= insert_json.dt_upto.as_generic_type():
                labels.append(current)
                current += datetime.timedelta(hours=1)
        elif insert_json.group_type.as_generic_type() == 'day':
            while current <= insert_json.dt_upto.as_generic_type():
                labels.append(current)
                current += datetime.timedelta(days=1)
        elif insert_json.group_type.as_generic_type() == 'month':
            while current <= insert_json.dt_upto.as_generic_type():
                labels.append(current)
                next_month = (current.month % 12) + 1
                next_year = current.year + (current.month // 12)
                current = current.replace(year=next_year, month=next_month)
        dataset = []
        counter = 0
        len_aggregated_data = len(aggregated_data)

        # Соотнесение и заполнение пустых пространств в ответе mongo
        if insert_json.group_type.as_generic_type() == 'month':
            for i in range(len(labels)):
                if counter < len_aggregated_data and labels[i].year == aggregated_data[counter][0].year and labels[i].month == aggregated_data[counter][0].month:
                    dataset.append(aggregated_data[counter][1])
                    counter += 1
                else:
                    dataset.append(0)
                labels[i] = labels[i].strftime("%Y-%m-%dT%H:%M:%S")
        if insert_json.group_type.as_generic_type() == 'day':
            for i in range(len(labels)):
                if counter < len_aggregated_data and labels[i].year == aggregated_data[counter][0].year and labels[i].month == aggregated_data[counter][0].month and labels[i].day == aggregated_data[counter][0].day:
                    dataset.append(aggregated_data[counter][1])
                    counter += 1
                else:
                    dataset.append(0)
                labels[i] = labels[i].strftime("%Y-%m-%dT%H:%M:%S")
        if insert_json.group_type.as_generic_type() == 'hour':
            for i in range(len(labels)):
                if counter < len_aggregated_data and labels[i].year == aggregated_data[counter][0].year and labels[i].month == aggregated_data[counter][0].month and labels[i].day == aggregated_data[counter][0].day and labels[i].hour == aggregated_data[counter][0].hour:
                    dataset.append(aggregated_data[counter][1])
                    counter += 1
                else:
                    dataset.append(0)
                labels[i] = labels[i].strftime("%Y-%m-%dT%H:%M:%S")

        return OutputJSON(dataset=dataset, labels=labels)
