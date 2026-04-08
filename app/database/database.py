from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from .base import metadata
import asyncio
import os

CONNECTION = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(
    CONNECTION,
    pool_size=2,
    max_overflow=0,
    pool_timeout=30
    )

session = sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

class Database:
    def __init__(self) -> None:
        self.session: Optional[Session] = None

    def __aenter__(self):
        self.session = Session()
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def init_db():
    from app.models.user_model import User
    from app.models.post_model import Post
    from app.models.comment_model import Comment

    with engine.begin() as conn:
        conn.run(metadata.create_all())

if __name__ == "__main__":
    init_db()
