import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory of the current file (app/config.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up TWO levels to reach /Users/muhammmadaasimdogar/learn/
# (One level to 'fastapi/', another to 'learn/')
env_path = os.path.join(current_dir, "..", "..", ".env")

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=env_path)

settings = Settings()