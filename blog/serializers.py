from rest_framework import serializers

from .models import BlogPost, Comment


class BlogPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "body", "created_at"]


class BlogPostListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "comments_count", "created_at"]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "comments", "created_at"]

    def get_comments(self, obj):
        MAX_COMMENTS = 10
        comments = obj.comments.order_by("-created_at")[:MAX_COMMENTS]
        return CommentSerializer(comments, many=True).data
