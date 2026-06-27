# Installation Guide

This guide covers how to set up EnterpriseIQ on your local machine for development or evaluation.

## Prerequisites
- **Python 3.10** or higher.
- **Git**.
- Optional: **Docker** (if you prefer containerised setups).

## Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/enterpriseiq/enterprise-knowledge-intelligence-platform.git
   cd enterprise-knowledge-intelligence-platform
   ```

2. **Create a Virtual Environment**
   We strongly recommend using a virtual environment to isolate dependencies.
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the required packages. Using the `[dev,llm]` flag installs testing tools and Anthropic integration.
   ```bash
   pip install -e ".[dev,llm]"
   ```

4. **Verify Installation**
   Ensure the CLI is accessible.
   ```bash
   enterprise-rag --help
   ```

## Using Docker

If you prefer not to manage Python environments, you can use the provided Makefile to build and run the Docker image.

```bash
make docker-build
make docker-run
```
The API will be available at `http://localhost:8000`.
