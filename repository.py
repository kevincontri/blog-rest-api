from models import User, Post, Comment
from database import db_connect

class UserRepository:

    @staticmethod
    def get_user_by_username(username):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""SELECT id, password_hash
                     FROM users
                     WHERE username = ?""",
                     (username,)
                  )
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def create_user(user: User):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""INSERT INTO users (id, username, password_hash, created_at)
                     VALUES (?, ?, ?, ?)""",
                     (user.id, user.username, user.password_hash, user.created_at)
                  )
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(user_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""SELECT id, username, created_at 
                     FROM users 
                     WHERE id = ?""",
                     (user_id,)
                 )
        row = c.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    @staticmethod
    def get_all_users():
        conn = db_connect()
        c = conn.cursor()
        c.execute("""SELECT id, username, created_at 
                     FROM users"""
                 )
        all_users = c.fetchall()
        conn.close()
        return [dict(user) for user in all_users]


class PostRepository:

    @staticmethod
    def create_post(post: Post):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""INSERT INTO posts 
                     VALUES (?, ?, ?, ?, ?)""",
                  (post.id, post.title, post.content,
                  post.author_id, post.created_at)
                 )
        conn.commit()
        conn.close()

    @staticmethod
    def get_post_query(author_id=None, search=None, sort_by=None, page=1, limit=10):
        conn = db_connect()
        c = conn.cursor()
        query = """SELECT users.username as 'post_author', title, posts.content, users.id as 'author_id', posts.created_at as 'post_date', posts.id as 'post_id'
                   FROM posts 
                   JOIN users ON users.id = posts.author_id 
                   WHERE 1=1"""
        params = []

        if author_id:
            query += " AND author_id = ?"
            params.append(author_id)

        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")

        if sort_by in ["created_at", "title"]:
            query += f" ORDER BY posts.{sort_by}"

        query += " LIMIT ? OFFSET ?"

        offset = (page - 1) * limit
        params.extend([limit, offset])
        c.execute(query, params)

        rows = c.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    @staticmethod
    def get_post(post_id: str):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""SELECT users.username as 'post_author', title, posts.content, users.id as 'author_id', posts.created_at as 'post_date', posts.id as 'post_id'
                     FROM posts 
                     JOIN users ON users.id = posts.author_id 
                     WHERE posts.id = ?""",
                  (post_id,))
        post = c.fetchone()
        conn.close()
        return post

    @staticmethod
    def update_title(title, post_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""UPDATE posts 
                     SET title = ? 
                     WHERE id = ?""",
                     (title, post_id)
                 )
        conn.commit()
        conn.close()

    @staticmethod
    def update_content(content, post_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""UPDATE posts 
                     SET content = ? 
                     WHERE id = ?""",
                     (content, post_id)
                 )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_post(post_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def is_post_from_user(post_id: str, author_id: str):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""SELECT * 
                     FROM posts
                     WHERE id = ?
                     AND author_id = ?""",
                     (post_id, author_id)
                  )
        row = c.fetchone()
        conn.close()
        return row if row else None

class CommentRepository:

    @staticmethod
    def create_comment(comment: Comment):
        conn = db_connect()
        c = conn.cursor()
        c.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?)",
                  (comment.id, comment.content, comment.post_id,
                  comment.author_id, comment.created_at))
        conn.commit()
        conn.close()

    @staticmethod
    def get_comments_by_post(post_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("SELECT id, content, post_id, author_id, created_at FROM comments WHERE post_id = ?", (post_id,))
        all_comments = c.fetchall()
        conn.close()
        return [dict(comment) for comment in all_comments]

    @staticmethod
    def get_comment(comment_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("SELECT content, created_at, id as 'comment_id', author_id, post_id  FROM comments WHERE id = ?", (comment_id,))
        comment = c.fetchone()
        conn.close()
        return dict(comment) if comment else None

    @staticmethod
    def delete_comment(comment_id):
        conn = db_connect()
        c = conn.cursor()
        c.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def is_comment_from_user(comment_id: str, user_id: str):
        conn = db_connect()
        c = conn.cursor()
        c.execute("""SELECT * 
                     FROM comments
                     WHERE id = ?
                     AND author_id = ?""",
                     (comment_id, user_id)
                  )
        row = c.fetchone()
        conn.close()
        return row if row else None
