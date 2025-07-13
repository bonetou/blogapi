import pytest
from rest_framework.test import APIClient
from blog.models import BlogPost, Comment
import uuid

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def blog_post():
    return BlogPost.objects.create(title="Test Title", content="Test content")


def test_create_post_success(api_client):
    payload = {"title": "New Post", "content": "Content"}
    response = api_client.post("/api/posts", payload, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "New Post"


def test_create_post_validation_error(api_client):
    payload = {"title": ""}
    response = api_client.post("/api/posts", payload, format="json")
    assert response.status_code == 400
    assert "content" in response.data


def test_list_posts_with_comment_count(api_client, blog_post):
    Comment.objects.create(post=blog_post, body="Nice comment")
    response = api_client.get("/api/posts")
    assert response.status_code == 200
    assert response.data["results"][0]["comments_count"] == 1


def test_retrieve_post_success(api_client, blog_post):
    Comment.objects.create(post=blog_post, body="Comment 1")
    response = api_client.get(f"/api/posts/{blog_post.id}")
    assert response.status_code == 200
    assert response.data["title"] == blog_post.title
    assert len(response.data["comments"]) == 1


def test_retrieve_post_404(api_client):
    non_existent_id = uuid.uuid4()
    response = api_client.get(f"/api/posts/{non_existent_id}")
    assert response.status_code == 404


def test_add_comment_success(api_client, blog_post):
    payload = {"body": "Great post!", "author": "Henrique"}
    response = api_client.post(f"/api/posts/{blog_post.id}/comments", payload, format="json")
    assert response.status_code == 201
    assert response.data["author"] == "Henrique"


def test_add_comment_missing_fields(api_client, blog_post):
    payload = {}
    response = api_client.post(f"/api/posts/{blog_post.id}/comments", payload, format="json")
    assert response.status_code == 400
    assert "body" in response.data


def test_add_comment_to_nonexistent_post(api_client):
    non_existent_id = uuid.uuid4()
    payload = {"body": "Oops", "author": "X"}
    response = api_client.post(f"/api/posts/{non_existent_id}/comments", payload, format="json")
    assert response.status_code == 404


def test_create_post_internal_error(api_client, monkeypatch):
    def raise_exception(*args, **kwargs):
        raise Exception("Unexpected failure")

    monkeypatch.setattr("blog.views.BlogPostListCreateView.create", raise_exception)

    payload = {"title": "Crash", "content": "This should fail"}
    response = api_client.post("/api/posts", payload, format="json")

    assert response.data == {"detail": "Internal server error."}
    assert response.status_code == 500
