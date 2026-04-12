from app.repository.user_repo import UserRepository
from app.security.auth import hash_password, verify_password
from app.exceptions.exceptions import *

user_repo = UserRepository()


class UserService:    
    def verify_credentials(self, username: str, password: str) -> dict:
        rows = user_repo.get_user_by_username(username)
        if rows:
            if verify_password(password, rows["password_hash"]):
                return rows
            raise WrongCredentials("Wrong password")
        raise NotFoundError("User not found")

    def create_user(self, username: str, password: str) -> dict:
        hashed = hash_password(password)
        new_user = user_repo.create_user(username, hashed)
        return new_user

    def get_all_users(self) -> list[dict]:
        return user_repo.get_all_users()

    def get_user(self, user_id: int) -> dict | None:
        user = user_repo.get_user(user_id)
        if user:
            return user
        raise NotFoundError("User not found")
    
    def get_user_posts(self, user_id: int) -> list[dict]:
        posts = user_repo.get_user_posts(user_id)
        if not posts:
            return []
        return posts
