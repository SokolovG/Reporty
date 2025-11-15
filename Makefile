migration:
	docker compose exec backend uv run alembic revision --autogenerate -m "$(msg)"

migrate:
	docker compose exec backend uv run alembic upgrade head

create_admin:
	docker compose exec backend uv run python -m backend.src.cli.create_admin
