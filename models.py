import uuid
from datetime import datetime

class User:
    def __init__(self, username: str):
        self.id = str(uuid.uuid4())
        self.username = username
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at
        }

class Post:
    def __init__(self, title: str, content: str, author_id: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at
        }

class Comment:
    def __init__(self, content: str, post_id: str, author_id: str):
        self.id = str(uuid.uuid4())
        self.content = content
        self.post_id = post_id
        self.author_id = author_id
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id,
            "author_id": self.author_id,
            "created_at": self.created_at
        }