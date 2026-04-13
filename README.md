# Blog REST API

## Update v3.0:
- New code structure following an MVC pattern.
- SQLAlchemy integration.
- Improved responses for each request, with more relevant data.

A backend service in a REST-style for managing users, posts and comments using `FastAPI`. This project demonstrates fundamental backend development concepts, such as:

* RESTful routing
* Layered architecture in MVC pattern
* Request and response validation with Pydantic
* SQL-based persistence with SQLAlchemy integration.
* Relational logic (users, posts and comments)
* HTTP status handling with FastAPI
* JWT Authentication and Authorization

This application allows creation of users, authoring of posts, and commenting on posts, with authentication ensuring users can only modify their own content.

## Stack

* Python
* FastAPI
* Pydantic
* SQL
* Uvicorn

## Dependencies
* JWT (Authentication)
* bcrypt (password hashing)

## Project Structure

* `app.py` - API layer (HTTP routes and request/response handling)
* `services.py` - Business logic for users, posts and comments
* `repository.py` - Database access layer (SQL queries)
* `database.py` - SQLite connection and table initialization
* `models.py` - Domain entities (`User`, `Post` and `Comment`)
* `schemas.py` - Pydantic models for request and response validation
* `auth.py` - JWT token creation and verification
* `requirements.txt` - Dependencies

## Installation

Clone the repository:

```
git clone https://github.com/kevincontri/blog-rest-api.git
cd blog-rest-api
```

Create and activate virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Run the server

```
uvicorn app:app --reload
```

Open interactive docs:

```
http://127.0.0.1:8000/docs
```

---

## Authentication

This API uses JWT Bearer token authentication. Protected routes require a valid token in the `Authorization` header.

### Register

`POST /users`

Request body:
```json
{
  "username": "john",
  "password": "john123"
}
```

### Login

`POST /auth/login`

Request body:
```json
{
  "username": "john",
  "password": "john123"
}
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

Use the returned token as a Bearer token in subsequent request headers:
```
Authorization: Bearer eyJhbGc...
```

---

## API User Endpoints

### Get all users

`GET /users`

Response:
```json
[
  {
    "id": "uuid",
    "username": "john",
    "created_at": "timestamp"
  }
]
```

### Get a specific user

`GET /users/{user_id}`

Returns user information.

---

## API Post Endpoints

### Create a post (Authentication needed)

`POST /posts`

The author is determined from the token.

Request body:
```json
{
  "title": "My first post",
  "content": "Hello World!"
}
```

Response:
```json
{
  "id": "uuid",
  "title": "My first post",
  "content": "Hello World!",
  "author_id": "uuid",
  "created_at": "timestamp"
}
```

### Get all posts

`GET /posts`

Supports optional query parameters:

| Parameter | Type | Description |
|---|---|---|
| `author_id` | string | Filter posts by author |
| `search` | string | Search by title |
| `sort_by` | string | Sort by `title` or `created_at` |
| `page` | int | Page number (default: 1) |
| `limit` | int | Results per page (default: 10) |

### Get a specific post

`GET /posts/{post_id}`

Returns post information with author details.

### Edit a post (Authentication needed)

`PATCH /posts/{post_id}`

Only the post's author can edit it.

Request body (any combination of fields):
```json
{
  "title": "Updated title",
  "content": "Updated content"
}
```

### Delete a post (Authentication needed)

`DELETE /posts/{post_id}`

Only the post's author can delete it.

Response:
```json
{
  "message": "Post Deleted Successfully"
}
```

---

## API Comment Endpoints

### Create a comment (Authentication needed)

`POST /posts/{post_id}/comments`

The author is determined from the token.

Request body:
```json
{
  "content": "Great post!"
}
```

Response:
```json
{
  "comment_id": "uuid",
  "content": "Great post!",
  "author_id": "uuid",
  "post_id": "uuid",
  "created_at": "timestamp"
}
```

### Get all comments for a post

`GET /posts/{post_id}/comments`

Returns all comments associated with the given post.

### Delete a comment (Authentication needed)

`DELETE /comments/{comment_id}`

Only the comment's author can delete it.

Response:
```json
{
  "message": "Comment deleted successfully"
}
```

---

## Future Improvements

* Migrate to PostgreSQL for production readiness
* Add refresh tokens for better session management
