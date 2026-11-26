
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # These values are provided by Docker Compose.
    database_user: str = "f1_user"
    database_password: str = "local_dev_password"
    database_name: str = "f1_analytics"

    # "postgres" is the service name in docker-compose.yml.
    database_host: str = "postgres"
    database_port: int = 5432


# One settings object shared by the application.
settings = Settings()
