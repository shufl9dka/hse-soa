import os


class AppConfig:
    SQL_ENGINE_URI = os.getenv("SQL_ENGINE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    POSTS_SERVICE_ADDR = os.getenv("POSTS_SERVICE_ADDR")
