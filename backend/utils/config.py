from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAPI_URL: str = Field(default='/openapi.json')
    SWAGGER_URL: str = Field(default='/docs')
    REDOC_URL: str = Field(default='/redoc')

    class Config:
        env_file = ".env"


settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        _ = settings
    except ValidationError as e:
        raise Exception("Invalid environment variables") from e
    yield
