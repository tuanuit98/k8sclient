from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = True
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "supersecretkey"

    class Config:
        env_file = ".env"

settings = Settings()
