runserver:
	poetry run python manage.py runserver

requirements:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

.PHONY: runserver requirements migrations migrate