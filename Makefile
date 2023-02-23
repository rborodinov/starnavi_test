.PHONY: build dev up-dev bash up-dev bot up_bot


build: dev bot

dev:
	docker compose build dev

up:
	docker compose up dev

bash:
	docker compose run --entrypoint=bash dev

bot:
	docker compose build bot

up_bot:
	docker compose up bot

bash_bot:
	docker compose run --entrypoint=bash bot