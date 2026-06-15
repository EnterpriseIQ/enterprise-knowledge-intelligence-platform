"""Command-line interface for the Enterprise RAG platform.

Examples
--------
    python -m src.cli --build
    python -m src.cli --role HR    --query "What is the remote work policy?"
    python -m src.cli --user eng_dave --query "Show finance budget allocations."
"""
from __future__ import annotations

import argparse
import json

from src.pipeline import RAGPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Secure Enterprise RAG CLI")
    parser.add_argument("--query", "-q", help="Question to ask.")
    parser.add_argument("--role", "-r", help="Role: Admin|HR|Finance|Engineering|Compliance")
    parser.add_argument("--user", "-u", help="Known user id (overrides role lookup).")
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--build", action="store_true", help="Build the index and exit.")
    parser.add_argument("--json", action="store_true", help="Emit full JSON result.")
    args = parser.parse_args()

    pipeline = RAGPipeline()
    stats = pipeline.build_index()
    if args.build or not args.query:
        print("Index built:", json.dumps(stats, indent=2))
        if not args.query:
            return

    result = pipeline.query(args.query, role=args.role,
                            user_id=args.user or "", top_k=args.top_k)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
        return

    print(f"\nQ: {result.query}")
    print(f"Role: {result.role}   Confidence: {result.confidence['label']} "
          f"({result.confidence['score']})")
    print(f"\nAnswer:\n{result.answer}\n")
    print("Citations:")
    for c in result.citations:
        print(f"  {c['reference']}")
    print(f"\nRouting: {result.route['rationale']}")
    print(f"Access: {result.authorised_count} authorised / "
          f"{result.denied_count} denied chunks")


if __name__ == "__main__":
    main()
