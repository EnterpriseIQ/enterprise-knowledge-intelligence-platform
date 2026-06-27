# Screenshots Specification: EnterpriseIQ

To convey a world-class engineering product, our screenshots must be meticulously crafted. They should not be raw window captures; they must be composed, perfectly cropped, and styled to match top-tier dev tools (like Linear, Vercel, or Warp).

## 1. Terminal / CLI Screenshots

**Theme:** Tokyo Night or Vercel Dark. Font: JetBrains Mono or Fira Code (size 14).
**Window:** Clean, borderless, macOS style traffic lights in the top left (or hidden entirely for a cleaner look).
**Padding:** 32px of padding inside the terminal window to give the text breathing room.
**Background:** A very subtle, dark radial gradient (e.g., `#0A0A0A` to `#000000`) behind the terminal window to make it pop.

### Shot 1.1: The Core Value Prop (RBAC in Action)
*   **Command:** `enterprise-rag --role "Analyst" --query "What is the Q3 revenue?"`
*   **Output:** Beautifully formatted CLI output (using Rich). Show the retrieval process, a bolded `[SECURITY: 3 chunks filtered by RBAC]`, and the final answer citing `finance_report_q3.pdf`.
*   **Purpose:** Proves the security filtering works instantly.

### Shot 1.2: The Offline Startup
*   **Command:** `docker-compose up`
*   **Output:** Show the startup logs indicating `Loading local embeddings...`, `Connecting to offline ChromaDB...`, `API running on :8000`.
*   **Purpose:** Proves the air-gapped, zero-dependency nature of the platform.

## 2. API / Developer Experience Screenshots

**Tool:** Insomnia or Postman (Dark Mode), or a highly styled Swagger UI.
**Layout:** 2-pane view. Request on left, Response on right.

### Shot 2.1: The Explainable API Response
*   **Request:** `POST /query` with a complex JSON body.
*   **Response:** Highlight the `access_summary` and `source_coverage` objects in the JSON payload, showing exactly how the engine arrived at its answer.
*   **Purpose:** Demonstrates that EnterpriseIQ is not a black box; it provides full observability to developers.

### Shot 2.2: IDE Integration
*   **Tool:** VS Code (Vercel Theme).
*   **File:** `main.py`
*   **Content:** A developer instantiating the `RAGPipeline` and calling `agentic_query()`. Show strong TypeScript/Python type-hinting popups (e.g., Pylance showing the return type as `QueryResult`).
*   **Purpose:** Highlights the excellent Developer Experience (DX) and strict typing.

## 3. Web UI / Dashboard Screenshots

**Browser:** Safari (clean top bar) or a stylized borderless browser window.
**Size:** 2560x1440 (scaled down for web).

### Shot 3.1: The Agentic RAG Interface
*   **Layout:** A chat-like interface on the left, and a "Reasoning Trace" panel on the right.
*   **Data:** A query like "Summarize the architectural changes in the new billing system."
*   **Trace Panel:** Shows the step-by-step agent workflow: `Classifying Intent -> Retrieving from Confluence -> Retrieving from GitHub -> Reranking -> Synthesizing`.
*   **Purpose:** Makes the complex LangGraph backend visually understandable to users.

### Shot 3.2: Analytics & Observability
*   **Layout:** A Grafana-style dashboard (or our custom UI).
*   **Data:** Charts showing "Queries per Department", "RBAC Denials over Time", and "Average Retrieval Latency (ms)".
*   **Purpose:** Appeals to enterprise buyers and operations teams who need to monitor system health and security.

## Best Practices for Capture
*   **Never use real data.** Create a highly realistic synthetic dataset (`Acme Corp`) with believable file names (`Q3_Earnings_Transcript.pdf`, `users_table.sql`).
*   **Perfect sizing.** Export at 2x resolution (Retina) for crisp text on high-DPI displays.
*   **Focus.** Use subtle blurring on background elements to draw the eye to the specific code line or UI element we want to highlight.