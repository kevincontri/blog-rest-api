from app.models.comment_model import Comment
from app.models.user_model import User
from app.database.database import Database
from sqlalchemy import insert, select, delete


class CommentRepository:

    def create_comment(self, content: str, post_id: int, author_id: int) -> dict:
        with Database() as db:
            query = (
                insert(Comment)
                .values(content=content, post_id=post_id, author_id=author_id)
                .returning(Comment)
            )
            result = db.session.execute(query)
            db.session.commit()
            inserted_comment = result.fetchone()
            formatted_comment = self.get_comment(inserted_comment.id)
            return formatted_comment

    def get_comments_by_post(self, post_id: int) -> list[dict]:
        with Database() as db:
            results = (
                db.session.query(
                    User.c.username,
                    User.c.id.label("user_id"),
                    Comment.c.content,
                    Comment.c.created_at,
                    Comment.c.id.label("comment_id"),
                )
                .join(Comment, User.c.id == Comment.c.author_id)
                .where(Comment.c.post_id == post_id)
                .all()
            )

            return [comment._asdict() for comment in results]

    def get_comment(self, comment_id: int) -> dict | None:
        with Database() as db:
            results = (
                db.session.query(
                    User.c.username,
                    User.c.id.label("user_id"),
                    Comment.c.content,
                    Comment.c.created_at,
                    Comment.c.id.label("comment_id"),
                )
                .join(Comment, User.c.id == Comment.c.author_id)
                .where(Comment.c.id == comment_id)
                .one_or_none()
            )

            if not results:
                return None
            return dict(results._mapping)

    def delete_comment(self, comment_id: int, user_id: int) -> bool:
        with Database() as db:
            query = (
                delete(Comment)
                .where(Comment.c.id == comment_id)
                .where(Comment.c.author_id == user_id)
            )
            db.session.execute(query)
            db.session.commit()
            return True

    def is_comment_from_user(self, comment_id: int, user_id: int) -> bool:
        with Database() as db:
            query = (
                select(Comment)
                .where(Comment.c.id == comment_id)
                .where(Comment.c.author_id == user_id)
            )
            result = db.session.execute(query)
            comment = result.one_or_none()
            return comment
