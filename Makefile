.PHONY: lint
## Run pre-commit checks
lint:
	poetry run pre-commit run --all-files

.PHONY: test
## Run the tests inside the container with pytest
test:
	docker-compose exec django pytest
