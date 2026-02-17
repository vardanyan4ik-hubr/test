.PHONY: help install run test lint format clean docker-build docker-up docker-down

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

run: ## Запустить приложение
	python -m src.main

test: ## Запустить тесты
	pytest tests/ -v --cov=src --cov-report=html

lint: ## Проверить код линтером
	flake8 src/
	mypy src/

format: ## Форматировать код
	black src/
	black tests/

clean: ## Очистить временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Собрать Docker образ
	docker-compose build

docker-up: ## Запустить контейнеры
	docker-compose up -d

docker-down: ## Остановить контейнеры
	docker-compose down

docker-logs: ## Показать логи контейнеров
	docker-compose logs -f

docker-shell: ## Войти в контейнер бота
	docker-compose exec bot bash

db-shell: ## Войти в PostgreSQL
	docker-compose exec db psql -U bot_user -d telegram_assyst_bot

redis-shell: ## Войти в Redis CLI
	docker-compose exec redis redis-cli
