from app.models.user_model import User
from app.models.post_model import Post
from app.database.database import Database
from sqlalchemy import insert, select


class UserRepository:

    def get_user_by_username(self, username) -> dict | None:
        with Database() as db:
            query = select(User).where(User.c.username == username).limit(1)
            result = db.session.execute(query)
            user = result.one_or_none()
            if user:
                return dict(user._mapping)
            return None

    def create_user(self, username: str, password_hash: str) -> dict:
        with Database() as db:
            query = (
                insert(User)
                .values(username=username, password_hash=password_hash)
                .returning(User)
            )
            result = db.session.execute(query)
            db.session.commit()
            inserted_user = result.fetchone()
            return dict(inserted_user._mapping)

    def get_user(self, user_id: int) -> dict | None:
        with Database() as db:
            result = db.session.query(
                User.c.username,
                User.c.id,
                User.c.created_at,
            ).where(User.c.id == user_id)

            user = result.one_or_none()
            if user:
                return dict(user._mapping)

    def get_all_users(self) -> list[dict]:
        with Database() as db:
            query = select(User)
            result = db.session.execute(query)
            users = result.all()
            return [dict(user._mapping) for user in users]

    def get_user_posts(self, user_id: int) -> list[dict]:
        with Database() as db:
            query = select(Post).where(Post.c.author_id == user_id)
            result = db.session.execute(query)
            posts = result.all()
            return [dict(post._mapping) for post in posts]
