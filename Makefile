format:
	ruff check --select I --fix && ruff format

build:
	docker compose down --rmi all && \
	docker builder prune -f && \
	docker compose up --build

clear:
	docker compose down --rmi all && \
	docker builder prune -f

run:
	docker compose up

delete_dir:
	find . -type d -name "$(dir)" -exec rm -r {} +

delete_files:
	find . -name "$(file)" -delete
