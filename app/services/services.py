from app.repository.repository import UserRepository, PostRepository, CommentRepository
from app.models import User, Post, Comment
from app.security.auth import hash_password, verify_password



class PostService():

    def create_post(self, title, content, author_id):
        user_service = UserService()
        user_exists = user_service.get_user(author_id)
        if user_exists:
            new_post = Post(title, content, author_id)
            PostRepository.create_post(new_post)
            return new_post
        return None

    def get_post(self, post_id):
        return PostRepository.get_post(post_id)

    def update_post(self, post_id, user_id, title=None, content=None):
        post_owner = PostRepository.is_post_from_user(post_id, user_id)
        if post_owner:
            if title is not None:
                PostRepository.update_title(title, post_id)
            if content is not None:
                PostRepository.update_content(content, post_id)
            return PostRepository.get_post(post_id)
        return None

    def delete_post(self, post_id, user_id):
        post_owner = PostRepository.is_post_from_user(post_id, user_id)
        if post_owner:
            PostRepository.delete_post(post_id)
            return True
        return None

    def get_post_query(self, author_id, search, sort_by, page, limit):
        query = PostRepository.get_post_query(author_id, search, sort_by, page, limit)
        if query:
            return query
        else:
            return []

class CommentService():

    def create_comment(self, post_id, user_id, content):
        user_service = UserService()
        user = user_service.get_user(user_id)

        post_service = PostService()
        post = post_service.get_post(post_id)

        if post is not None and user is not None:
            new_comment = Comment(content, post_id, user_id)
            CommentRepository.create_comment(new_comment)
            return new_comment
        return None

    def get_comments_from_post(self, post_id):
        post_service = PostService()
        post = post_service.get_post(post_id)
        if post:
            return CommentRepository.get_comments_by_post(post_id)
        return None

    def get_comment(self, comment_id):
        return CommentRepository.get_comment(comment_id)

    def delete_comment(self, comment_id, user_id):
        comment_owner = CommentRepository.is_comment_from_user(comment_id, user_id)
        if comment_owner:
            CommentRepository.delete_comment(comment_id)
            return True
        return None


