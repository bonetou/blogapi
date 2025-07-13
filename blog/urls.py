from django.urls import path
from .views import BlogPostListCreateView, BlogPostRetrieveView, CommentCreateView, CommentListView

urlpatterns = [
    path("posts", BlogPostListCreateView.as_view(), name="post-list-create"),
    path("posts/<uuid:pk>", BlogPostRetrieveView.as_view(), name="post-retrieve"),
    path("posts/<uuid:pk>/comments", CommentCreateView.as_view(), name="comment-create"),
    path("posts/<uuid:pk>/comments/", CommentListView.as_view(), name="comment-list"),
]
