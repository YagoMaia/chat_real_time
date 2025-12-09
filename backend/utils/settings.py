from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    MONGO_URL: str = "mongodb://localhost:27017/"
    DATABASE_NAME : str = "chat_real_time"
    COLLECTION_NAME : str = "messages"

settings = Settings()
