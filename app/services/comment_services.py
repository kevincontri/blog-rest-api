from app.models.comment_model import Comment
from app.repository.comment_repo import CommentRepository
from app.services.post_services import PostService
from app.database.database import Database
from sqlalchemy import insert, select
from app.exceptions.exceptions import NotFoundError

post_service = PostService()
comment_repo = CommentRepository()


class CommentService:

    def create_comment(self, post_id: int, user_id: int, content: str) -> dict:
        post_service.get_post(post_id)
        new_comment = comment_repo.create_comment(content, post_id, user_id)
        return new_comment

    def get_comments_from_post(self, post_id: int) -> list[dict]:
        post_service.get_post(post_id)
        return comment_repo.get_comments_by_post(post_id)

    def get_comment(self, comment_id: int):
        comment = comment_repo.get_comment(comment_id)
        if not comment:
            raise NotFoundError("Comment not found")
        return comment

    def delete_comment(self, comment_id: int, user_id: int):
        comment_owner = comment_repo.is_comment_from_user(comment_id, user_id)
        if not comment_owner:
            raise NotFoundError("Comment not found")
        comment_repo.delete_comment(comment_id, user_id)
        return True
