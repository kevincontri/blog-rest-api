from app.models.user_model import User
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
            query = select(User).where(User.c.id == user_id).limit(1)
            result = db.session.execute(query)
            user = result.one_or_none()
            if user:
                return dict(user._mapping)
            return None

    def get_all_users(self) -> list[dict]:
        with Database() as db:
            query = select(User)
            result = db.session.execute(query)
            users = result.all()
            return [dict(user._mapping) for user in users]
