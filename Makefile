.PHONY: build dev up-dev bash up-dev


build: dev

dev:
	docker compose build dev

up:
	docker compose up dev

bash:
	docker compose run --entrypoint=bash dev
