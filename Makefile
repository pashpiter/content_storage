app-up:
	@echo "Starting FastAPI app ..."
	cd app && uvicorn main:app --reload

up:
	@echo "Docker compose up"
	docker compose up -d --build

stop:
	@echo "Docker compose stop"
	docker compose stop

restart:
	docker compose down && \
	docker volume rm content_storage_postgres_data && \
	docker volume rm content_storage_redis_data && \
	docker volume rm content_storage_app_static_data && \
	docker compose up -d --build