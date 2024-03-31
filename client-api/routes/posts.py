import grpc
from protobuf_to_dict import protobuf_to_dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import Optional
from pydantic import BaseModel

import posts_pb2, posts_pb2_grpc
from utils.config import AppConfig
from utils.depends import on_current_user

router = APIRouter(prefix="/posts")


class CreatePostModel(BaseModel):
    text: str


class UpdatePostModel(BaseModel):
    post_id: str
    text: Optional[str] = None


class GetDeleteModel(BaseModel):
    post_id: str


class ListPostsModel(BaseModel):
    page: int


@router.post("/create")
async def create_post(
    data: CreatePostModel,
    user_id: int = Depends(on_current_user),
):
    status = "ok"
    async with grpc.aio.insecure_channel(AppConfig.POSTS_SERVICE_ADDR) as channel:
        stub = posts_pb2_grpc.PostsStub(channel)
        response = await stub.CreatePost(posts_pb2.Post(
            creator_id=user_id,
            text=data.text,
        ))
        if response.http_status // 100 != 2:
            status = "error"

    return JSONResponse({
        "status": status,
        "message": response.message,
        "post_id": response.post_id,
    }, status_code=response.http_status)


@router.post("/update")
async def update_post(
    data: UpdatePostModel,
    user_id: int = Depends(on_current_user),
):
    status = "ok"
    async with grpc.aio.insecure_channel(AppConfig.POSTS_SERVICE_ADDR) as channel:
        stub = posts_pb2_grpc.PostsStub(channel)
        response = await stub.UpdatePost(posts_pb2.UpdateRequest(
            post_id=data.post_id,
            text=data.text,
            user_id=user_id,
        ))
        if response.http_status // 100 != 2:
            status = "error"

    return JSONResponse({
        "status": status,
        "message": response.message,
        "post_id": response.post_id,
    }, status_code=response.http_status)


@router.post("/delete")
async def delete_post(
    data: GetDeleteModel,
    user_id: int = Depends(on_current_user),
):
    status = "ok"
    async with grpc.aio.insecure_channel(AppConfig.POSTS_SERVICE_ADDR) as channel:
        stub = posts_pb2_grpc.PostsStub(channel)
        response = await stub.DeletePost(posts_pb2.GetDeleteRequest(
            post_id=data.post_id,
            user_id=user_id,
        ))
        if response.http_status // 100 != 2:
            status = "error"

    return JSONResponse({
        "status": status,
        "message": response.message,
        "post_id": response.post_id,
    }, status_code=response.http_status)


@router.get("/get")
async def get_post(
    data: GetDeleteModel,
    user_id: int = Depends(on_current_user),
):
    status = "ok"
    async with grpc.aio.insecure_channel(AppConfig.POSTS_SERVICE_ADDR) as channel:
        stub = posts_pb2_grpc.PostsStub(channel)
        response = await stub.GetPost(posts_pb2.GetDeleteRequest(
            post_id=data.post_id,
            user_id=user_id,
        ))
        if response.http_status // 100 != 2:
            status = "error"

    return JSONResponse({
        "status": status,
        "message": response.message,
        "post": protobuf_to_dict(response.post) if response.post else None,
    }, status_code=response.http_status)


@router.get("/list")
async def list_posts(
    data: ListPostsModel,
    user_id: int = Depends(on_current_user),
):
    async with grpc.aio.insecure_channel(AppConfig.POSTS_SERVICE_ADDR) as channel:
        stub = posts_pb2_grpc.PostsStub(channel)
        response = await stub.ListPosts(posts_pb2.ListRequest(
            page=data.page,
            user_id=user_id,
        ))

    return JSONResponse({
        "status": "ok",
        "posts": [protobuf_to_dict(post) for post in response.posts] if response.posts else None,
    }, status_code=response.http_status)
