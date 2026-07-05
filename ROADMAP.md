# EnterpriseIQ Roadmap

This roadmap outlines the planned features, architectural improvements, and strategic goals for the EnterpriseIQ platform.

## Q1 - Current Release (v1.0)
- ✅ Core RAG Pipeline Implementation
- ✅ Strict Two-Layer RBAC
- ✅ Extractive Offline Generation Mode
- ✅ FastAPI Backend with API Key Authentication
- ✅ Initial React/Vite Frontend Interface
- ✅ Synthetic Data Generator for Evaluation

## Q2 - Search & Ranking Enhancements
- 🔄 **Cross-Encoder Reranking:** Implement a cross-encoder model (e.g., `ms-marco-MiniLM-L-6-v2`) to improve top-K precision before generation.
- 🔄 **Advanced Chunking:** Introduce semantic boundary chunking to replace the current fixed-size overlapping strategy.
- ⏳ **Graph RAG Integration:** Experiment with LangGraph for more complex, multi-step reasoning workflows over the knowledge base.

## Q3 - Identity & Access
- ⏳ **SSO Integration:** Native support for Azure AD (Entra ID), Okta, and generic OIDC providers.
- ⏳ **Dynamic Access Control:** Move away from static `access_policies.json` to a dynamic, database-backed ACL management system.
- ⏳ **Audit Log Export:** Stream audit logs directly to SIEM systems (Splunk, Datadog) via OpenTelemetry.

## Q4 - Generative Capabilities & UI
- ⏳ **Local LLM Native Support:** Deep integration with Ollama to bundle local LLM generation (Llama 3, Mistral) with zero configuration.
- ⏳ **Admin Dashboard:** A comprehensive UI for managing users, inspecting audit logs, and tuning the `HYBRID_ALPHA` parameter visually.
- ⏳ **Streaming Responses:** Support Server-Sent Events (SSE) for streaming generated answers to the frontend in real-time.

---
*Note: This roadmap is subject to change based on community feedback and enterprise client requirements.*
