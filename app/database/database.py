from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from .base import metadata
import os
import dotenv

dotenv.load_dotenv()

CONNECTION = os.getenv("DATABASE_URL", "sqlite3:///database.db")

engine = create_engine(CONNECTION)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    
class Database:
    def __init__(self) -> None:
        self.session: Optional[Session] = None

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()


def init_db():
    from app.models.user_model import User
    from app.models.post_model import Post
    from app.models.comment_model import Comment

    metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
