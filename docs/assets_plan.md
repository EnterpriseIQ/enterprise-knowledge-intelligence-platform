# Comprehensive Visual Asset and Output Plan

This document details the production specifications for visual assets, product demos, screenshots, and recruiter experiences necessary for a world-class launch.

## 1. Visual Assets (Part 3)

| Asset Name | Specification | Description |
| :--- | :--- | :--- |
| **Hero Image** | `2400x1200`, PNG/WebP | A sleek, dark-mode abstract visualization of structured and unstructured data converging into a single glowing knowledge graph, representing the "Fused Index". The branding color `#009688` should highlight the connection paths. |
| **Dashboard Mockup** | `2560x1440` | A high-fidelity screenshot of a mock React dashboard showing the hybrid search in action, highlighting the citation numbers and the RBAC clearance banner ("Viewing as: HR"). |
| **Architecture Diagram (Hero)** | SVG, transparent background | A stylized, isometric view of the EnterpriseIQ data pipeline, from raw data (PDF, SQL, JSON) to the ChomaDB vector store, to the LangGraph orchestration layer. |
| **Feature Illustrations** | 4x SVGs, `500x500` | Minimalist line-art illustrations representing: 1. Zero-Trust RBAC (a shield over a database), 2. Hybrid Retrieval (intersecting waves and text), 3. Offline Mode (a severed cloud with a glowing local server), 4. Grounded Citations (a document with magnifying glass and a checkmark). |
| **Social OpenGraph Image** | `1200x630` | Bold typography "Enterprise Knowledge Intelligence", the EnterpriseIQ logo, and a subtle code snippet in the background showing the FastAPI endpoint definition. |
| **Logo/Favicon** | SVG / `512x512` | An abstract letter 'E' merging with a magnifying glass or neural network node. |
| **Loading Animations** | Lottie / JSON | A pulse animation on a document icon representing "Scanning vectors..." |

## 2. Product Demos (Part 4)

*   **3-Minute Demo (GIF/MP4):**
    *   *Script:* Start in terminal. Run `python run_demo.py --role HR`. Show retrieving HR policy. Switch role to `Engineer`. Show retrieval of GitHub PRs. Try to retrieve HR policy as Engineer -> Show the explicit "Access Denied" or filtered result.
    *   *Focus:* Proving the Zero-Trust RBAC.
*   **10-Minute Technical Walkthrough (YouTube):**
    *   *Script:* Start with the `docs/architecture/system.md`. Show the `docker-compose.yml`. Boot the server. Jump into a Jupyter Notebook demonstrating the `HybridRetriever` directly, showing the exact BM25 + Dense vector score blending.
    *   *Focus:* Developer Experience and code transparency.
*   **Enterprise/Investor Demonstration:**
    *   *Script:* Use the React frontend (`http://localhost:4173/enterprise-knowledge-intelligence-platform/`). Upload a 100-page simulated SOC2 compliance PDF. Ask a complex question: "What are our password rotation requirements?". Show the exact extracted snippet, the page number, and the confidence score. Disconnect the internet to prove offline capability.
*   **GitHub README GIF:**
    *   A high-speed, 15-second loop of the CLI performing a hybrid search with citations appearing in green text.

## 3. Screenshots (Part 5)

1.  **Terminal Execution (Theme: One Dark Pro)**
    *   *Angle:* Straight on, slight drop shadow on a macOS window frame.
    *   *Content:* The output of `uvicorn src.api.main:app`, showing the fast startup time and loaded models.
2.  **API Swagger Docs**
    *   *Browser Size:* `1440x900`
    *   *Content:* Expanded POST `/query` endpoint, showing the request body schema (`query`, `role`, `user_id`).
3.  **Local Dashboard**
    *   *Browser Size:* `1920x1080`
    *   *Content:* The React UI displaying a search result with multiple citations linking to different source types (PDF and SQL).

## 4. Recruiter Experience (Part 10)
If Staff Engineers from OpenAI or Anthropic review this repository, the following should stand out:
*   **First Impressions:** The `README.md` is enterprise-ready, explaining *why* it exists (RBAC, offline), not just *how* to run it. The use of FastAPI, LangGraph, and ChromaDB shows a modern, production-focused stack.
*   **Strengths:** Explicit handling of citations and hallucinations via `Extractive Mode`. The rigorous RBAC testing in `tests/test_rbac.py` proves it's not a toy.
*   **Improvements Addressed:**
    *   *Linting & Types:* Ensured 100% ruff compliance and strict typing.
    *   *Accessibility:* Added full WAI-ARIA support to Framer Motion components in the React UI.
    *   *Security:* Prevented SQL Injection in the ingestion loader and Timing Attacks in the API key validation.
