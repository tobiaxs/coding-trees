.PHONY: lint
## Run pre-commit checks
lint:
	poetry run pre-commit run --all-files

.PHONY: test
## Run the tests inside the container with pytest
test:
	docker-compose exec django pytest


.PHONY: makemigrations
## Run the makemigrations command
makemigrations:
	docker-compose exec django python manage.py makemigrations


.PHONY: migrate
## Run the migrate command
migrate:
	docker-compose exec django python manage.py migrate
