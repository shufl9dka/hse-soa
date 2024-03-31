from models.post import PostData
import posts_pb2


def post_model_to_proto(post: PostData) -> posts_pb2.Post:
    return posts_pb2.Post(
        id=post.id,
        creator_id=post.creator_id,
        text=post.text,
        created_at=post.created_at,
        edited_at=post.edited_at,
    )
