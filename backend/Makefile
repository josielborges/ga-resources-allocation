.PHONY: setup-db migrate seed-data start-db stop-db

# Database setup (migrations + seed)
setup-db:
	python scripts/setup_db.py

# Run migrations only
migrate:
	alembic upgrade head

# Reset database (clear existing data + seed)
seed-data:
	python scripts/seed_data.py

# Start PostgreSQL container
start-db:
	cd docker/db && docker-compose up -d

# Stop PostgreSQL container
stop-db:
	cd docker/db && docker-compose down

# Create new migration
migration:
	alembic revision --autogenerate -m "$(msg)"

# Install dependencies
install:
	pip install -r requirements.txt

# Full setup (install + start db + setup)
full-setup: install start-db setup-db