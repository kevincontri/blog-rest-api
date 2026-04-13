# Blog REST API

## Update v3.0:

- New code structure following an MVC pattern.
- SQLAlchemy integration.
- Improved responses for each request, with more relevant data.
- Dependency injection in API routes.
- Integraded APIRouters for better organization of routes.

A backend service in a REST-style for managing users, posts and comments using `FastAPI`. This project demonstrates fundamental backend development concepts, such as:

- RESTful routing
- Layered architecture in MVC pattern
- Request and response validation with Pydantic
- SQL-based persistence with SQLAlchemy integration.
- Relational logic (users, posts and comments)
- HTTP status handling with FastAPI
- JWT Authentication and Authorization

This application allows creation of users, authoring of posts, and commenting on posts, with authentication ensuring users can only modify their own content.

## Stack

- Python
- FastAPI
- Pydantic
- SQL
- Uvicorn

## Dependencies

- JWT (Authentication)
- bcrypt (password hashing)

## Project Structure

- `/controllers/*` - API layer (HTTP routes and request/response handling for authentication, comments, posts and users)
- `/database/*` - SQLAlchemy engine and context connection
- `/exceptions/exceptions` - Error handling with proper responses
- `/models/*` - Creation of comment, post and user tables for SQLAlchemy integration.
- `/repository/*` - Database manipulation and queries (select, insert, update, delete) for each table.
- `/schemas/*` - Pydantic BaseModels for formatted API responses.
- `/security/auth` - JWT authentication and password hashing and verification.
- `/server/server` - FastAPI entrance, with APIRouters included and database initialization.
- `/services/*` - Connection between repositories and controllers, validating responses and raising exceptions if necessary.
- `requirements.txt` - Dependencies
- `run.py` - Entry point of application, runs the FastAPI server.

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
python run.py
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
    "id": "1",
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
  "id": "1",
  "title": "My first post",
  "content": "Hello World!",
  "author_id": "1",
  "created_at": "timestamp"
}
```

### Get all posts

`GET /posts`

Supports optional query parameters:

| Parameter   | Type   | Description                     |
| ----------- | ------ | ------------------------------- |
| `author_id` | string | Filter posts by author          |
| `search`    | string | Search by title                 |
| `sort_by`   | string | Sort by `title` or `created_at` |
| `page`      | int    | Page number (default: 1)        |
| `limit`     | int    | Results per page (default: 10)  |

### Get a specific post

`GET /posts/{post_id}`

Returns post information with author details and post comments.

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

Responds with status code 204 No Content, indicating success in the operation.

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
  "comment_id": "1",
  "content": "Great post!",
  "author_id": "uuid",
  "post_id": "1",
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

- Dockerize application.
- Add refresh tokens for better session management
