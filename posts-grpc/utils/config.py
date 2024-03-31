import os


class AppConfig:
    SQL_ENGINE_URI = os.getenv("SQL_ENGINE_URI")
    GRPC_PORT = int(os.getenv("GRPC_PORT"))
    POSTS_PAGE_SIZE = int(os.getenv("POSTS_PAGE_SIZE"))
