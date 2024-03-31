import time
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.post import PostData
import posts_pb2, posts_pb2_grpc
from utils.config import AppConfig
from utils.transforms import post_model_to_proto


class PostsServicer(posts_pb2_grpc.PostsServicer):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def CreatePost(self, request: posts_pb2.Post, context) -> posts_pb2.PostResponse:
        post = PostData(
            id=str(uuid.uuid4()),
            creator_id=request.creator_id,
            text=request.text,
            created_at=int(time.time()),
        )
        async with self.session_maker() as session:
            async with session.begin():
                session.add(post)
                await session.commit()
        return posts_pb2.PostResponse(http_status=201, message="Post created successfully", post_id=post.id)


    async def UpdatePost(self, request: posts_pb2.UpdateRequest, context) -> posts_pb2.PostResponse:
        async with self.session_maker() as session:
            async with session.begin():
                post = await session.execute(
                    select(PostData).where(PostData.id == request.post_id)
                )
                post = post.scalar_one_or_none()
                if post is None:
                    return posts_pb2.PostResponse(http_status=404, message="Post was not found", post_id=request.post_id)
                if request.user_id != post.creator_id:
                    return posts_pb2.PostResponse(http_status=401, message="You can't access this post", post_id=request.post_id)

                if request.text:
                    post.text = request.text
                post.edited_at = int(time.time())
                await session.commit()

        return posts_pb2.PostResponse(http_status=200, message="Post updated successfully", post_id=request.post_id)

    async def DeletePost(self, request: posts_pb2.GetDeleteRequest, context) -> posts_pb2.PostResponse:
        async with self.session_maker() as session:
            async with session.begin():
                post = await session.execute(
                    select(PostData).where(PostData.id == request.post_id)
                )
                post = post.scalar_one_or_none()
                if post is None:
                    return posts_pb2.PostResponse(http_status=404, message="Post was not found", post_id=request.post_id)
                if request.user_id != post.creator_id:
                    return posts_pb2.PostResponse(http_status=401, message="You can't access this post", post_id=request.post_id)

                await session.delete(post)
                await session.commit()

        return posts_pb2.PostResponse(http_status=200, message="Post removed successfully", post_id=request.post_id)

    async def GetPost(self, request: posts_pb2.GetDeleteRequest, context) -> posts_pb2.GetPostResponse:
        async with self.session_maker() as session:
            async with session.begin():
                post = await session.execute(
                    select(PostData).where(PostData.id == request.post_id)
                )
                post = post.scalar_one_or_none()
                if post is None:
                    return posts_pb2.GetPostResponse(http_status=404, message="Post was not found")
                if request.user_id != post.creator_id:
                    return posts_pb2.GetPostResponse(http_status=401, message="You can't access this post")
                await session.commit()

        return posts_pb2.GetPostResponse(http_status=200, post=post_model_to_proto(post))

    async def ListPosts(self, request: posts_pb2.ListRequest, context) -> posts_pb2.PostList:
        async with self.session_maker() as session:
            async with session.begin():
                query = await session.execute(
                    select(PostData)
                    .where(PostData.creator_id == request.user_id)
                    .order_by(PostData.created_at.desc())
                    .offset((request.page - 1) * AppConfig.POSTS_PAGE_SIZE)
                    .limit(AppConfig.POSTS_PAGE_SIZE)
                )
                posts = query.scalars().all()

        return posts_pb2.PostList(posts=[post_model_to_proto(post) for post in posts])
