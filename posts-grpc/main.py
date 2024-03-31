import asyncio
import grpc

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import posts_pb2_grpc

from models.base import Base
from servicers.posts import PostsServicer
from utils.config import AppConfig


async def on_startup(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    engine = create_async_engine(AppConfig.SQL_ENGINE_URI)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    posts_servicer = PostsServicer(async_session)

    await on_startup(engine)

    server = grpc.aio.server()
    posts_pb2_grpc.add_PostsServicer_to_server(posts_servicer, server)

    server.add_insecure_port(f"[::]:{AppConfig.GRPC_PORT}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(main())
