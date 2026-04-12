from sqlalchemy import Table, Column, Integer, String, ForeignKey
from datetime import datetime
from app.database.base import metadata

Comment = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String),
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("author_id", Integer, ForeignKey("users.id")),
    Column("created_at", String, default=lambda: datetime.now().isoformat()),
)
