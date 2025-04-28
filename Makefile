format:
	ruff check --select I --fix && ruff format

build:
	docker compose -f ./deploy/compose.yml down --rmi all && \
	docker builder prune -f && \
	docker compose -f ./deploy/compose.yml up --build

clear:
	docker compose -f ./deploy/compose.yml down --rmi all && \
	docker builder prune -f

run:
	docker compose -f ./deploy/compose.yml up

delete_dir:
	find . -type d -name "$(dir)" -exec rm -r {} +

delete_files:
	find . -name "$(file)" -delete
