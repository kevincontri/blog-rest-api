from app.repository.repository import UserRepository
from app.security.auth import hash_password, verify_password

class UserService():
    def verify_credentials(self, username, password):
        rows = UserRepository.get_user_by_username(username)
        if rows:
            if verify_password(password, rows[0]["password_hash"]):
                return rows
            return 2
        return 1

    def create_user(self, username, password):
        hashed = hash_password(password)
        new_user = UserRepository.create_user(username, hashed)
        return new_user

    def get_all_users(self):
        return UserRepository.get_all_users()

    def get_user(self, user_id):
        return UserRepository.get_user(user_id)