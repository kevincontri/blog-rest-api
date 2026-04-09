from app.models.comment_model import Comment
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
            return dict(inserted_comment._mapping)

    def get_comments_by_post(self, post_id: int) -> list[dict]:
        with Database() as db:
            query = select(Comment).where(Comment.c.post_id == post_id)
            result = db.session.execute(query)
            comments = result.all()
            return [dict(comment._mapping) for comment in comments]

    def get_comment(self, comment_id: int) -> dict | None:
        with Database() as db:
            query = select(Comment).where(Comment.c.id == comment_id).limit(1)
            result = db.session.execute(query)
            comment = result.one_or_none()
            if comment:
                return dict(comment._mapping)
            return None

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
