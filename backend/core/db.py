from typing import Any

from pymongo import AsyncMongoClient

from model import Message
from utils.settings import settings

# MONGO_URL: str = "mongodb://localhost:27017/"
# DATABASE_NAME : str = "chat_real_time"
# COLLECTION_NAME : str = "messages"

class MongoConnection:
    def __init__(self):
        self.client = AsyncMongoClient(settings.MONGO_URL)
        # await self.client.admin.command("ping")
        # print("Conexão feita com sucesso")


    async def insert_message(self, message: Message):
        """
        Function that insert a message in databse.
        """
        database = self.client[settings.DATABASE_NAME]
        collections = database[settings.COLLECTION_NAME]
        result = await collections.insert_one(message.model_dump(exclude={"id"}))
        return result.acknowledged

    async def get_all_no_delivered_messages(self, user_to: str ):
        """
        Function that get all no delivered messages for user_to.
        """
        try:
            database = self.client[settings.DATABASE_NAME]
            collections = database[settings.COLLECTION_NAME]
            all_messages :list[Message] = []
            cursor = collections.find({"user_to": user_to, "delivered": False})
            async for doc in cursor:
                all_messages.append(Message(**doc))
            return all_messages
        except Exception as error:
            print(f"Error get all no delivered messages: {error}")
            return []

    async def mark_message_as_delivered(self, message_id:Any):
        """
        Function that change status for delivered=False to delivered=True.
        """
        try:
            database = self.client[settings.DATABASE_NAME]
            collections = database[settings.COLLECTION_NAME]
            await collections.find_one_and_update(filter={"_id": message_id}, update={"$set": {"delivered": True}})
        except Exception as error:
            print(f"Error change status messages: {error}")

mongo_connection = MongoConnection()
