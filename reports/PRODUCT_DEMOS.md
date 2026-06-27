# Product Demo Scripts & Strategy: EnterpriseIQ

To position EnterpriseIQ as a top-tier enterprise AI platform, our product demos must be crisp, narrative-driven, and focused on our core differentiators: **Security (RBAC), Accuracy (Hybrid Search), and Offline Capability.**

## 1. The 3-Minute "Hook" Demo (For Landing Page & Social)

**Goal:** Immediately communicate value and differentiation to a general technical audience.
**Format:** High-paced, polished screen recording with voiceover and clean zooms.

*   **0:00 - 0:30 (The Problem):** Show a standard RAG pipeline hallucinating or leaking cross-department data. Voiceover: "Standard AI over enterprise data is a security nightmare."
*   **0:30 - 1:15 (The Solution - RBAC):** Open EnterpriseIQ CLI/UI. Execute a query as `Role: Engineering`. The answer is highly technical. Immediately execute the exact same query as `Role: HR`. The platform strictly refuses or returns only publicly cleared policy data. Voiceover highlights the zero-trust architecture.
*   **1:15 - 2:00 (The Engine - Hybrid Search):** Search for a specific internal bug ID (e.g., `INC-8492`). Show how standard vector search misses it, but EnterpriseIQ's BM25 + Cross-Encoder hybrid search nails the exact document.
*   **2:00 - 3:00 (The Proof - Citations):** Zoom in on the generated answer. Click a citation link that directly opens the source PDF/SQL table highlighted to the exact text. Voiceover: "No hallucinations. Just grounded, verifiable intelligence. EnterpriseIQ."

## 2. The 10-Minute Technical Walkthrough (For DevRel & YouTube)

**Goal:** Prove to Staff/Principal Engineers that the architecture is sound and easy to deploy.
**Format:** Terminal and IDE-heavy screencast. "Code-first" approach.

*   **Setup (2 mins):** `git clone`, `docker-compose up`. Show how fast the system boots completely offline.
*   **Ingestion (2 mins):** Drop a PDF and a SQLite DB into the `data/` folder. Show the ingest script parsing and chunking in real-time.
*   **Pipeline Architecture (3 mins):** Open `src/pipeline.py` in VS Code. Walk through the `agentic_query` method. Highlight the clean orchestration between LangGraph, the Router, and the HybridRetriever.
*   **Security Deep Dive (3 mins):** Open `src/security/rbac.py`. Explain the pre-filter vs. post-filter approach. Run a curl request against the API showing the `access_decisions` audit trail in the JSON response.

## 3. The Enterprise Demonstration (For CIOs & CISOs)

**Goal:** Assure executives that the platform meets strict compliance and data governance standards.
**Format:** Slide-driven presentation leading into a high-level UI demo.

*   **Focus 1: Air-Gapped Execution:** Emphasize that no data ever leaves the VPC. Demonstrate the system running with the WiFi turned off.
*   **Focus 2: Auditability:** Show the `/audit` endpoint and Prometheus metrics. Explain how every query is logged with explicit "authorized" and "denied" chunk counts.
*   **Focus 3: Integration:** Discuss how it plugs into existing IdPs (Okta/Entra) rather than requiring a new user directory.

## 4. The Recruiter Demonstration (For Talent Acquisition)

**Goal:** Show prospective top-tier engineering talent that we are working on hard, interesting problems using modern tech.
**Format:** Interactive, exploratory session.

*   **Focus:** The complexity of the `CrossEncoderReranker` and the `HybridRetriever`.
*   **Narrative:** "We aren't just calling the OpenAI API. We are building custom inverted indices, managing dense/sparse fusions, and orchestrating local LLMs to solve latency and security bottlenecks at scale."

## 5. Investor Demonstration

**Goal:** Demonstrate massive TAM (Total Addressable Market) and immediate enterprise ROI.
**Format:** Story-driven.

*   **Narrative:** The "Before" and "After" of enterprise knowledge discovery. Show a mock employee spending hours searching Jira, Confluence, and PDFs. Show EnterpriseIQ answering the same complex, multi-source question in 300ms. Highlight the moat: the proprietary RBAC and hybrid ingestion engine.

## 6. Short-Form Demos (GIFs/WebM)

*   **GitHub README GIF:**
    *   *Visual:* A split-screen terminal. Left side: Querying as Admin (gets full financial report). Right side: Querying as Intern (gets "Access Denied" for financials, but successfully queries public handbook).
    *   *Duration:* 12 seconds.
*   **Landing Page GIF:**
    *   *Visual:* A beautiful, sleek input bar. User types a query. The UI instantly expands showing: 1) Intent classification, 2) Documents retrieved, 3) RBAC filtering out 3 documents, 4) Final grounded answer generation.
    *   *Duration:* 8 seconds.