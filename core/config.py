from pydantic_settings import BaseSettings
from pathlib import Path
class Settings(BaseSettings):
    DB_USER:str
    DB_HOST:str
    DB_PORT:str
    DB_PASSWORD:str
    DB_NAME:str
    DB_DRIVER:str
    DB_DIALECT:str
    KAFKA_BOOTSTRAP_SERVERS: str
    api:str
    email:str
    


    def get_db_url(self):
        return f"{self.DB_DIALECT}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

    class Config:
        env_file=Path(__file__).parent.parent / ".env"


setting=Settings()

