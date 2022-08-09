runserver:
	poetry run python manage.py runserver

requirements:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 pollequiz

test:
	poetry run python manage.py test pollequiz

test-cov: 
	poetry run coverage run manage.py test
	poetry run coverage xml

.PHONY: runserver requirements migrations migrate lint test test-cov