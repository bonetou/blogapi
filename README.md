# Blog API

This is a RESTful API for a simple blogging platform. It allows clients to manage blog posts and their associated comments. The application is built with Django, Django REST Framework, PostgreSQL, and includes pagination, API schema generation, and Swagger documentation.

## Requirements

* Python 3.12+ (use [pyenv](https://github.com/pyenv/pyenv) or [uv](https://github.com/astral-sh/uv))
* PostgreSQL
* Docker and Docker Compose (for database setup)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/blogapi.git
cd blogapi
```

### 2. Create and activate a virtual environment

```bash
uv venv --python 3.12
```
Or Just

```bash
python -m venv .venv
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```
For Windows users, use:
```bash
# For Windows users
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

or using uv:
```bash
uv pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:
Run: 
```bash
cp .env.example .env
```

### 5. Start PostgreSQL using Docker Compose

```bash
docker compose up -d db
```

### 6. Run migrations

```bash
make make-migrations
make migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
make runserver
```

### 9. Access the application

* Swagger UI: [http://localhost:8000/v1/api/swagger](http://localhost:8000/v1/api/swagger)

## JWT Authentication

Obtain a token:
- Use your superuser credentials or create a new user via the Django admin interface.

```bash
curl -X POST http://localhost:8000/v1/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# This will return a JSON response with an access token.
#{
#  "access": "your_access_token",
#  "refresh": "your_refresh_token"
#}
```

Use the token:

```bash
curl http://localhost:8000/v1/api/posts/ \
  -H "Authorization: Bearer your_access_token"
```

## Running Tests

```bash
make test
```

## Linting
```bash
make lint
```

## Next Steps

If more time were available, the following improvements would be implemented:

* Improve authorization logic with granular permission policies and throttling
* Permissions and rate limiting
* Add background tasks with Celery
* Tagging and category support for posts
* Search and filtering by post title or content
* Caching for frequently accessed data
* Establish CI/CD pipelines for automated testing and deployment
