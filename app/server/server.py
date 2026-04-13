from fastapi import FastAPI
from app.database.database import init_db
from app.controllers import (
    comment_controller,
    post_controller,
    user_controller,
    auth_controller,
)

app = FastAPI(
    title="Blog REST API",
    version="3.0",
    description="RESTful Blog API in Python using FastAPI and SQL with JWT authentication, layered architecture, and role-based resource ownership.",
)

init_db()

app.include_router(user_controller.router)
app.include_router(post_controller.router)
app.include_router(comment_controller.router)
app.include_router(auth_controller.router)
app.include_router(comment_controller.router2)
