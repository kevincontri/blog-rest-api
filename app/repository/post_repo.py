from app.models.post_model import Post
from app.models.user_model import User
from app.models.comment_model import Comment
from app.database.database import Database
from sqlalchemy import insert, select, desc, update, delete


class PostRepository:

    def create_post(self, title: str, content: str, author_id: int) -> dict:
        with Database() as db:
            query = (
                insert(Post)
                .values(title=title, content=content, author_id=author_id)
                .returning(Post)
            )
            result = db.session.execute(query)
            db.session.commit()
            inserted_post = result.fetchone()
            return dict(inserted_post._mapping)

    def get_post_query(
        self, page: int, limit: int, author_id=None, search=None, sort_by=None
    ) -> list[dict]:
        with Database() as db:
            query = db.session.query(
                User.c.username,
                Post.c.title,
                Post.c.content,
                User.c.id,
                Post.c.created_at,
                Post.c.id,
            ).join(User, User.c.id == Post.c.author_id)

            if author_id:
                query = query.where(Post.c.author_id == author_id)

            if search:
                query = query.where(Post.c.title.ilike(f"%{search}%"))

            if sort_by == "created_at":
                query = query.order_by(desc(Post.c.created_at))

            elif sort_by == "title":
                query = query.order_by(Post.c.title)

            offset = (page - 1) * limit

            results = query.limit(limit).offset(offset).all()

            return [row._asdict() for row in results]

    def get_post(self, post_id: str) -> dict | None:
        with Database() as db:
            query = select(Post).where(Post.c.id == post_id)
            result = db.session.execute(query)
            post = result.one_or_none()
            if post:
                return dict(post._mapping)
            return None

    def update_post(self, post_id: int, title: str = None, content: str = None) -> dict:
        with Database() as db:
            query = update(Post).where(Post.c.id == post_id)

            if title:
                query = query.values(title=title)
            if content:
                query = query.values(content=content)
            query = query.returning(Post)
            result = db.session.execute(query)
            db.session.commit()
            updated_post = result.fetchone()
            return dict(updated_post._mapping)

    def delete_post(self, post_id: int) -> bool:
        with Database() as db:
            query = delete(Post).where(Post.c.id == post_id)
            db.session.execute(query)
            db.session.commit()
            return True

    def is_post_from_user(self, post_id: int, author_id: int):
        with Database() as db:
            query = (
                select(Post)
                .where(Post.c.id == post_id)
                .where(Post.c.author_id == author_id)
            )
            result = db.session.execute(query)
            post = result.one_or_none()
            return post

    def get_comments_from_post(self, post_id: int) -> list[dict]:
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
