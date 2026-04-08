from sqlalchemy import Table, Column, Integer, String, ForeignKey
from datetime import datetime
from app.database.base import metadata

Post = Table(
  "posts",
  metadata,
  Column("id", Integer, primary_key=True),
  Column("title", String),
  Column("content", String),
  Column("author_id", Integer, ForeignKey("users.id")),
  Column("created_at", String, default=lambda: datetime.now().isoformat()),
)