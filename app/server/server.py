from fastapi import FastAPI
from app.controllers import (
    comment_controller,
    post_controller,
    user_controller,
    auth_controller,
)

app = FastAPI(
    title="Blog REST API",
    version="2.0",
    description="RESTful Blog API in Python using FastAPI and SQLite with JWT authentication, layered architecture, and role-based resource ownership.",
)

app.include_router(user_controller.router)
app.include_router(post_controller.router)
app.include_router(comment_controller.router)
app.include_router(auth_controller.router)
