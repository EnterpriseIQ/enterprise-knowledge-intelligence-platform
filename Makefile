# Secure Enterprise RAG Intelligence Platform — developer task runner
.DEFAULT_GOAL := help
.PHONY: help install data build run demo test lint docker-build docker-run clean

PYTHON ?= python
PORT ?= 8000
IMAGE ?= enterprise-rag-platform:latest

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies (runtime + dev)
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e ".[dev]"

data:  ## Generate the synthetic enterprise corpus
	$(PYTHON) -m data.generate_data

build: data  ## Build the vector index (smoke test)
	$(PYTHON) -m src.cli --build

run: data  ## Run the FastAPI server (http://localhost:$(PORT), docs at /docs)
	uvicorn src.api.main:app --host 0.0.0.0 --port $(PORT) --reload

demo: data  ## Run the end-to-end demo (queries + RBAC proof + audit)
	$(PYTHON) run_demo.py

test: data  ## Run the test suite
	$(PYTHON) -m pytest

lint:  ## Lint with ruff (if installed)
	ruff check src tests data || echo "ruff not installed; run 'make install'"

docker-build:  ## Build the Docker image
	docker build -t $(IMAGE) .

docker-run:  ## Run the container (maps port $(PORT))
	docker run --rm -p $(PORT):8000 $(IMAGE)

clean:  ## Remove caches and regenerable runtime artifacts
	rm -rf .pytest_cache .ruff_cache **/__pycache__ src/**/__pycache__ \
		data/vectorstore data/logs/audit_trail.jsonl
	find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
