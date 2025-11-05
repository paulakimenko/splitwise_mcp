# Splitwise MCP Service - Makefile

.PHONY: help docker-compose-build docker-compose-up docker-compose-down docker-compose-logs-tail unit-test lint format check install-dev clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Docker Commands
docker-build: ## Build Docker image for the application
	@if [ -f .env ]; then set -o allexport; source .env; set +o allexport; fi && \
	REGISTRY=$${DOCKER_REGISTRY:-paulakimenko} && \
	IMAGE_NAME=$${DOCKER_IMAGE_NAME:-splitwise-mcp} && \
	TAG=$${DOCKER_TAG:-latest} && \
	echo "Building Docker image: $$REGISTRY/$$IMAGE_NAME:$$TAG" && \
	docker build -t $$REGISTRY/$$IMAGE_NAME:$$TAG .

docker-push: ## Push Docker image to registry
	@if [ -f .env ]; then set -o allexport; source .env; set +o allexport; fi && \
	REGISTRY=$${DOCKER_REGISTRY:-paulakimenko} && \
	IMAGE_NAME=$${DOCKER_IMAGE_NAME:-splitwise-mcp} && \
	TAG=$${DOCKER_TAG:-latest} && \
	echo "Pushing Docker image: $$REGISTRY/$$IMAGE_NAME:$$TAG" && \
	docker push $$REGISTRY/$$IMAGE_NAME:$$TAG

docker-build-push: docker-build docker-push ## Build and push Docker image

docker-run: ## Run Docker container locally (without database - limited functionality)
	@if [ -f .env ]; then set -o allexport; source .env; set +o allexport; fi && \
	REGISTRY=$${DOCKER_REGISTRY:-paulakimenko} && \
	IMAGE_NAME=$${DOCKER_IMAGE_NAME:-splitwise-mcp} && \
	TAG=$${DOCKER_TAG:-latest} && \
	echo "⚠️  Running standalone container (no database) - limited functionality" && \
	echo "💡 Use 'make docker-compose-up' for full functionality with MongoDB" && \
	echo "Running Docker container: $$REGISTRY/$$IMAGE_NAME:$$TAG" && \
	docker run --rm -p 8000:8000 --env-file .env $$REGISTRY/$$IMAGE_NAME:$$TAG

docker-run-full: ## Run with docker-compose (recommended - includes MongoDB)
	@echo "🚀 Starting full stack with MongoDB..." && \
	make docker-compose-up && \
	echo "✅ Service available at http://localhost:8000" && \
	echo "📚 API docs at http://localhost:8000/docs" && \
	echo "🔍 Health check: curl http://localhost:8000/health"

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

# Virtual Environment Setup
venv: ## Create virtual environment
	python -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

venv-activate: ## Show activation command for virtual environment
	@echo "To activate virtual environment, run: source .venv/bin/activate"

# Development Commands
install-dev: ## Install development dependencies
	@if [ ! -d ".venv" ]; then echo "Virtual environment not found. Run 'make venv' first."; exit 1; fi
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements-dev.txt

unit-test: ## Run unit tests only
	.venv/bin/python -m pytest tests/ -v --tb=short --ignore=tests/integration

integration-test: ## Run integration tests (requires SPLITWISE_API_KEY)
	@echo "Running integration tests against live Splitwise API..."
	@echo "⚠️  This will create and delete a test group in your Splitwise account"
	@if [ -f .env ]; then set -o allexport; source .env; set +o allexport; fi && \
	if [ -z "$$SPLITWISE_API_KEY" ] && [ -z "$$SPLITWISE_CONSUMER_KEY" ]; then echo "Error: Either SPLITWISE_API_KEY or SPLITWISE_CONSUMER_KEY/SPLITWISE_CONSUMER_SECRET must be set"; exit 1; fi && \
	.venv/bin/python -m pytest tests/integration/ -v --tb=short -s

integration-test-docker: ## Run integration tests with Docker Compose (MongoDB + live API)
	@echo "Starting MongoDB with Docker Compose..."
	@docker-compose up -d mongo
	@echo "Waiting for MongoDB to be ready..."
	@sleep 5
	@echo "Running integration tests against live Splitwise API with Docker MongoDB..."
	@if [ -f .env ]; then set -o allexport; source .env; set +o allexport; fi && \
	if [ -z "$$SPLITWISE_API_KEY" ] && [ -z "$$SPLITWISE_CONSUMER_KEY" ]; then echo "Error: Either SPLITWISE_API_KEY or SPLITWISE_CONSUMER_KEY/SPLITWISE_CONSUMER_SECRET must be set"; exit 1; fi && \
	MONGO_URI=mongodb://localhost:27017 .venv/bin/python -m pytest tests/integration/ -v --tb=short -s
	@echo "Stopping Docker Compose services..."
	@docker-compose down

test-all-local: ## Run unit tests and integration tests
	$(MAKE) unit-test
	$(MAKE) integration-test

unit-test-coverage: ## Run unit tests with coverage report
	.venv/bin/python -m pytest tests/ -v --tb=short --cov=app --cov-report=html --cov-report=term --ignore=tests/integration

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
test-all: check unit-test ## Run all checks and unit tests (no integration)

test-full: check unit-test integration-test ## Run all checks, unit tests, and integration tests

ci: install-dev test-all ## Run full CI pipeline locally (unit tests only)

ci-full: install-dev test-full ## Run full CI pipeline with integration tests

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
setup: venv install-dev env-setup ## Full development setup
	@echo "Development environment setup complete!"
	@echo "1. Activate virtual environment: source .venv/bin/activate"
	@echo "2. Update .env file with your SPLITWISE_API_KEY"
	@echo "3. Run 'make dev' to start the development server"
	@echo "4. Run 'make test-all' to run unit tests and checks"
	@echo "5. Run 'make integration-test' to run integration tests (requires API key)"