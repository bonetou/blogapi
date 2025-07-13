import uuid

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from blog.models import BlogPost, Comment

pytestmark = pytest.mark.django_db

@pytest.fixture(scope="module")
def user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user, _ = User.objects.get_or_create(username="testuser")
        user.set_password("testpass")
        user.save()
        return user


@pytest.fixture
def auth_client(user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def blog_post():
    return BlogPost.objects.create(title="Test Title", content="Test content")


def test_create_post_success(auth_client):
    payload = {"title": "New Post", "content": "Content"}
    response = auth_client.post("/v1/api/posts", payload, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "New Post"


def test_create_post_validation_error(auth_client):
    payload = {"title": ""}
    response = auth_client.post("/v1/api/posts", payload, format="json")
    assert response.status_code == 400
    assert "content" in response.data


def test_list_posts_with_comment_count(auth_client, blog_post):
    Comment.objects.create(post=blog_post, body="Nice comment")
    response = auth_client.get("/v1/api/posts")
    assert response.status_code == 200
    assert response.data["results"][0]["comments_count"] == 1


def test_retrieve_post_success(auth_client, blog_post):
    Comment.objects.create(post=blog_post, body="Comment 1")
    response = auth_client.get(f"/v1/api/posts/{blog_post.id}")
    assert response.status_code == 200
    assert response.data["title"] == blog_post.title
    assert len(response.data["comments"]) == 1


def test_retrieve_post_404(auth_client):
    non_existent_id = uuid.uuid4()
    response = auth_client.get(f"/v1/api/posts/{non_existent_id}")
    assert response.status_code == 404


def test_add_comment_success(auth_client, blog_post):
    payload = {"body": "Great post!", "author": "Henrique"}
    response = auth_client.post(f"/v1/api/posts/{blog_post.id}/comments", payload, format="json")
    assert response.status_code == 201
    assert response.data["author"] == "Henrique"


def test_add_comment_missing_fields(auth_client, blog_post):
    payload = {}
    response = auth_client.post(f"/v1/api/posts/{blog_post.id}/comments", payload, format="json")
    assert response.status_code == 400
    assert "body" in response.data


def test_add_comment_to_nonexistent_post(auth_client):
    non_existent_id = uuid.uuid4()
    payload = {"body": "Oops", "author": "X"}
    response = auth_client.post(f"/v1/api/posts/{non_existent_id}/comments", payload, format="json")
    assert response.status_code == 404


def test_create_post_internal_error(auth_client, monkeypatch):
    def raise_exception(*args, **kwargs):
        raise Exception("Unexpected failure")

    monkeypatch.setattr("blog.views.BlogPostListCreateView.create", raise_exception)

    payload = {"title": "Crash", "content": "This should fail"}
    response = auth_client.post("/v1/api/posts", payload, format="json")

    assert response.data == {"detail": "Internal server error."}
    assert response.status_code == 500
