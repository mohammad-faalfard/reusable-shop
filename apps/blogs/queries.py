from apps.account.models import User

from .models import BlogCategory, Post, PostComment


def get_all_blog_posts():
    """Retrieve all active posts."""
    return Post.objects.select_related("category").prefetch_related("tags").filter(is_active=True)


def get_all_blog_categories():
    """Retrieve all active categories."""
    return BlogCategory.objects.filter(is_active=True)


def get_blog_category(id: int, is_active=True) -> BlogCategory | None:
    """Retrieve blog category if exist."""
    return BlogCategory.objects.filter(id=id, is_active=is_active).first()


def get_post_details_by_id(post_id: int) -> Post | None:
    """
    Fetches a single active blog post by its ID, including related category and tags.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        Post | None: The Post object if found and active, or None if the post does not exist or is inactive.
    """
    try:
        post = Post.objects.select_related("category").prefetch_related("tags").get(id=post_id, is_active=True)
        return post
    except Post.DoesNotExist:
        return None


def get_post_comments(post: object) -> list[PostComment]:
    """
    Fetch active comments for a specific post and include the total count.
    """

    comments = post.comments.filter(
        post=post,
        is_accepted=True,
        is_active=True,
    ).order_by("-created_at")

    return comments


def get_posts_by_category(category: object) -> list[Post]:
    """
    Fetches all active blog posts related to a specific category.
    """
    return category.posts.filter(is_active=True)


def has_bookmarked(user: User, post: Post):
    """Check if a bookmark is in database."""
    return post.bookmarks.filter(user=user).exists()


def create_post_comment(post: Post, sender: User, comment: str, reply: User = None) -> PostComment:
    """Create a new comment."""
    obj = PostComment.objects.create(
        post=post,
        sender=sender,
        reply=reply,
        text=comment,
        is_accepted=False,
    )
    return obj
