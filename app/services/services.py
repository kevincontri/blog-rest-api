from app.repository.repository import UserRepository, PostRepository, CommentRepository
from app.models import User, Post, Comment
from app.security.auth import hash_password, verify_password





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


