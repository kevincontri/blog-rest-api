from app.repository.post_repo import PostRepository
from app.exceptions.exceptions import NotFoundError

post_repo = PostRepository()


class PostService:

    def create_post(self, title: str, content: str, author_id: int) -> dict:
        new_post = post_repo.create_post(title, content, author_id)
        return new_post

    def get_post(self, post_id: int) -> dict:
        post = post_repo.get_post(post_id)
        if post:
            return post
        raise NotFoundError("Post not found")

    def update_post(self, post_id: int, user_id: int, title=None, content=None) -> dict:
        post_owner = post_repo.is_post_from_user(post_id, user_id)
        if post_owner:
            updated_post = post_repo.update_post(post_id, title, content)
            return updated_post
        raise NotFoundError("Post not found")

    def delete_post(self, post_id: int, user_id: int) -> bool:
        post_owner = post_repo.is_post_from_user(post_id, user_id)
        if post_owner:
            post_repo.delete_post(post_id)
            return True
        raise NotFoundError("Post not found")

    def get_post_query(
        self,
        author_id: int = None,
        search: str = None,
        sort_by: str = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict:
        query = post_repo.get_post_query(page, limit, author_id, search, sort_by)
        if query:
            return query
        raise NotFoundError("Post not found")
    
    def get_comments_from_post(self, post_id: int) -> list[dict]:
        comments = post_repo.get_comments_from_post(post_id)
        if not comments:
            return []
        return comments
