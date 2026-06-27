# CLI Documentation

EnterpriseIQ includes a command-line interface for quick testing and local query execution without spinning up the full FastAPI server.

## Installation
The CLI is installed automatically when you install the package:
```bash
pip install -e .
```

## Usage

```bash
enterprise-rag --help
```

### Basic Query
You must provide a `--role` and a `--query`.

```bash
enterprise-rag --role HR --query "What is the remote work policy?"
```

### Changing Top-K
You can limit the number of source chunks retrieved using `--top_k`.

```bash
enterprise-rag --role Engineering --query "List active incidents" --top_k 3
```

### Output
The CLI outputs the generated answer to `stdout`, followed by a formatted list of citations and the confidence score. It acts as a direct wrapper around `RAGPipeline.agentic_query()`.
