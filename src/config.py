"""App config."""
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Temp ML Application"
    app_description: str = "ML Process for your projects"

    default_location: str = "local"  # local or s3
    logger_name = "ml_logger"
    log_to_file: bool = False
    log_file_path: str = "/tmp/ml_template.log"

    temp_folder = "/tmp/ml_template/"

    valid_image_extensions = ["jpg", "jpeg", "png"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_config():
    return Settings()
