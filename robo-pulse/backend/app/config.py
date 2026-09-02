'''
Day 11
This file holds our centralized app settings and replaces
the os.environ.get functions scattered throughout
'''

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgressql+asyncpg://:password@localhost:5432/robopulse"

    '''no default here because a wrong secret key value can cause 
    the app to startup seemingly successfully, but with a 
    silent failure because it will pass an incorrect key
    value for our JWT'''
    secret_key: str

    frontend_origin: str = "http://localhost:5173"

    '''Tells pydantic settings to acutally read from 
    backend/.env and fill these field from it'''
    model_config = SettingsConfigDict(env_file=".env")

# This line will raise an error on startup if .env values aren't set
settings = Settings()