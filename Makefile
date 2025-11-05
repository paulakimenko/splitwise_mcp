# Splitwise MCP Service - Makefile

.PHONY: help docker-compose-build docker-compose-up docker-compose-down docker-compose-logs-tail unit-test lint format check install-dev clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Docker Compose Commands
docker-compose-build: ## Build Docker containers
	docker-compose build --no-cache

docker-compose-up: ## Start all services in background
	docker-compose up -d

docker-compose-down: ## Stop and remove all containers
	docker-compose down -v

docker-compose-logs-tail: ## Show and follow logs from all services
	docker-compose logs -f

docker-compose-restart: ## Restart all services
	docker-compose restart

# Development Commands
install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

unit-test:
	.venv/bin/python -m pytest tests/ -v --tb=short

unit-test-coverage: ## Run unit tests with coverage report
	.venv/bin/python -m pytest tests/ -v --tb=short --cov=app --cov-report=html --cov-report=term

# Code Quality Commands
lint: ## Run code linting with Ruff
	.venv/bin/python -m ruff check app/ tests/

lint-fix: ## Run code linting with Ruff and auto-fix issues
	.venv/bin/python -m ruff check app/ tests/ --fix

format: ## Format code with Ruff
	.venv/bin/python -m ruff format app/ tests/

format-check: ## Check code formatting without making changes
	.venv/bin/python -m ruff format app/ tests/ --check

check: format-check lint ## Run all code quality checks

fix: format lint-fix ## Format code and fix linting issues

# Combined Commands
test-all: check unit-test ## Run all checks and tests

ci: install-dev test-all ## Run full CI pipeline locally

# Environment Commands
env-setup: ## Copy .env.example to .env if it doesn't exist
	@if [ ! -f .env ]; then cp .env.example .env; echo ".env file created from .env.example"; else echo ".env file already exists"; fi

# Cleanup Commands
clean: ## Clean up temporary files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage .pytest_cache/ 2>/dev/null || true

# Development Server
dev: env-setup ## Start development server (requires .env file)
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker Development
docker-dev: docker-compose-up ## Start development environment with Docker
	@echo "Development environment started. API available at http://localhost:8000"
	@echo "MongoDB available at mongodb://localhost:27017"
	@echo "Run 'make docker-compose-logs-tail' to see logs"

docker-dev-stop: docker-compose-down ## Stop development environment

# Full development setup
setup: install-dev env-setup ## Full development setup
	@echo "Development environment setup complete!"
	@echo "1. Update .env file with your API keys"
	@echo "2. Run 'make dev' to start the development server"
	@echo "3. Run 'make test-all' to run all tests and checks"