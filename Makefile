.PHONY: up down build migrate seed shell test lint logs prod-up prod-down

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

migrate:
	docker compose exec web python manage.py migrate

seed:
	docker compose exec web python manage.py seed_data
	docker compose exec web python manage.py setup_roles

shell:
	docker compose exec web python manage.py shell

test:
	cd backend && python manage.py test

lint:
	cd backend && ruff check .

logs:
	docker compose logs -f

prod-up:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down
