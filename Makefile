format:
	ruff check --select I --fix && ruff format

build:
	docker compose down --rmi all && \
	docker builder prune -f && \
	docker compose up --build

clear:
	docker compose down --rmi all && \
	docker builder prune -f
