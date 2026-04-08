from sqlalchemy import Table, Column, Integer, String
from datetime import datetime
from app.database.base import metadata

User = Table(
  "users",
  metadata,
  Column("id", Integer, primary_key=True),
  Column("username", String),
  Column("password_hash", String),
  Column("created_at", String, default=lambda: datetime.now().isoformat()),
)