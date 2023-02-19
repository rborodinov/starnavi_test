from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "starnavi"
    mode: str
    dbpath: str

    class Config:
        env_file = f"starnavi/envs/{getenv('MODE')}.env"
