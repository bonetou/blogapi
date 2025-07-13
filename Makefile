runserver:
	python manage.py runserver

make-migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

test:
	pytest -v

lint:
	ruff check . --fix
