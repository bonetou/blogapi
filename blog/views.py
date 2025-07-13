from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Prefetch
from .models import BlogPost, Comment
from .serializers import (
    BlogPostCreateSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    CommentSerializer,
)
from http import HTTPMethod


class BlogPostListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == HTTPMethod.GET:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == HTTPMethod.POST:
            return BlogPostCreateSerializer
        return BlogPostListSerializer

    def get_queryset(self):
        return (
            BlogPost.objects.annotate(comments_count=Count("comments"))
            .prefetch_related(Prefetch("comments"))
            .order_by("-created_at")
        )


class BlogPostRetrieveView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogPostDetailSerializer
    queryset = BlogPost.objects.prefetch_related("comments")


class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        post = generics.get_object_or_404(BlogPost, pk=post_id)
        serializer.save(post=post)


class CommentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")
