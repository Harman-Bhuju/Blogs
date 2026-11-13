from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    # Controls whether SQLAlchemy prints SQL queries to the terminal.
    # Set to true in development to debug queries, false in production.
    DB_LOGGING: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()