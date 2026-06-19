# KnowledgeX Product Design Document

This document defines the comprehensive product design, branding, messaging, and user experience strategy for positioning KnowledgeX as a premium enterprise knowledge intelligence platform.

---

## PART 1: PRODUCT BRAND

**Product Name:** KnowledgeX (Retained/Refined), or **Axiom**, **Nucleus**, or **Kortex**. We will proceed with **Kortex**.
**Tagline:** The Intelligence Layer for Enterprise Knowledge.
**Elevator pitch:** Kortex securely unifies fragmented enterprise data into a single, intelligent graph. It answers complex questions across PDFs, databases, and logs with absolute accuracy, enforcing strict role-based access control inside the retrieval path. Zero hallucinations. Zero data leaks. Complete traceability.
**One sentence:** Kortex is a secure, hybrid-retrieval AI platform that safely brings reasoning and exact answers to isolated enterprise data silos.
**Three sentence story:** Enterprises store their most valuable knowledge in disconnected silos bound by strict access rules. Naive AI exposes this data or hallucinates answers, eroding trust and compromising security. Kortex solves this by embedding access control directly into the retrieval engine, delivering perfectly cited, grounded answers only from data the user is authorized to see.
**Brand personality:** Trustworthy, precise, sophisticated, and impossibly fast. It feels like an extension of a high-performance engineering team—methodical but powerful.
**Voice:** Authoritative, clear, and unpretentious. We speak to technical leaders and enterprise operators with equal respect.
**Tone:** Confident but never arrogant. Technical but accessible. We avoid buzzwords and focus on concrete mechanisms (e.g., "hybrid retrieval," "RBAC-enforced") over hype.

---

## PART 2: LANDING PAGE STRUCTURE

### 1. Hero
*   **Purpose:** Hook the visitor instantly, establish premium feel, and explain the core value.
*   **Headline:** The Secure Intelligence Layer for Enterprise Data.
*   **Copy direction:** Direct, benefit-driven, emphasizing security and intelligence. Focus on bringing AI to private data safely.
*   **Visual idea:** A subtle, dark-mode terminal window morphing into an elegant node-graph animation, representing fragmented data becoming unified and intelligent.

### 2. Problem
*   **Purpose:** Agitate the pain of siloed data and the danger of naive RAG/AI.
*   **Headline:** Your data is siloed. Naive AI makes it dangerous.
*   **Copy direction:** Acknowledge that giving an LLM access to everything is a data leak waiting to happen. Highlight hallucinations and access violations.
*   **Visual idea:** A split-screen graphic: On the left, a chaotic, leaking pipeline of documents; on the right, Kortex’s precise, governed, and gated pipeline.

### 3. Solution
*   **Purpose:** Introduce Kortex as the methodical, secure answer.
*   **Headline:** Grounded answers. Governed access.
*   **Copy direction:** Explain that Kortex enforces RBAC *before* generating answers, ensuring absolute compliance and exact citations.
*   **Visual idea:** A clean, glowing schematic of the Kortex architecture, highlighting the "RBAC Enforcement" gate.

### 4. Features
*   **Purpose:** Highlight the core technical and business capabilities.
*   **Headline:** Engineered for absolute trust.
*   **Copy direction:** Brief, punchy descriptions of hybrid retrieval, multi-source ingestion, and explainability.
*   **Visual idea:** A bento-box grid of sleek, glassmorphic cards with animated micro-interactions (e.g., hovering over "RBAC" shows a glowing lock).

### 5. Architecture
*   **Purpose:** Win over the engineers and CTOs.
*   **Headline:** A transparent, offline-first pipeline.
*   **Copy direction:** Detail the pipeline (Ingestion -> Chunking -> Embedding -> Vector Store -> Hybrid Retrieval -> RBAC -> Assembly -> Generation).
*   **Visual idea:** An interactive, step-by-step pipeline diagram. Clicking a step reveals code snippets and technical specs.

### 6. How it works
*   **Purpose:** Show the user journey from query to cited answer.
*   **Headline:** From unstructured query to verifiable truth.
*   **Copy direction:** A 1-2-3 step flow: Ask, Retrieve & Filter, Answer with Citations.
*   **Visual idea:** A beautiful UI mockup of a query being typed, followed by the system retrieving documents (with access denied badges on some), and finally the generated answer with inline `[1]` citations.

### 7. Demo
*   **Purpose:** Prove it works immediately.
*   **Headline:** See Kortex in action.
*   **Copy direction:** Minimal. Let the product speak.
*   **Visual idea:** An embedded, auto-playing high-fidelity terminal recording (using Asciinema or similar) showing a fast query and citation.

### 8. Use Cases
*   **Purpose:** Help different personas see themselves using the product.
*   **Headline:** One platform. Every department.
*   **Copy direction:** Tailored snippets for HR (policies), Engineering (logs), Finance (budgets), and Compliance (audit).
*   **Visual idea:** A tabbed interface switching between different user avatars and queries, instantly updating the UI mockup to show role-specific results.

### 9. Performance
*   **Purpose:** Assure users it scales and is fast.
*   **Headline:** Instant retrieval. Infinite scale.
*   **Copy direction:** Highlight dense/sparse min-max fusion speed and offline capabilities.
*   **Visual idea:** Real-time benchmarking graphs (e.g., latency ms vs. query complexity) with sleek neon lines.

### 10. Security
*   **Purpose:** Alleviate enterprise CISO concerns.
*   **Headline:** Security isn't an add-on. It's the engine.
*   **Copy direction:** Emphasize defence-in-depth, clearance levels, and explicit ACLs.
*   **Visual idea:** An animated padlock graphic that expands into a layered security model (Identity, Clearance, Access).

### 11. Developer Experience
*   **Purpose:** Show that it's a joy to deploy and extend.
*   **Headline:** Deploys in minutes. Adapts to your stack.
*   **Copy direction:** Focus on the FastAPI backend, CLI, Docker support, and offline-first nature.
*   **Visual idea:** A beautifully syntax-highlighted code block showing a simple `docker-compose up` and an API `curl` request.

### 12. Enterprise Features
*   **Purpose:** Upsell the commercial value.
*   **Headline:** Built for the Fortune 500.
*   **Copy direction:** Mention SSO, OIDC, audit analytics, and SLA guarantees.
*   **Visual idea:** Subtle, premium metallic gradients behind text listing enterprise features.

### 13. Roadmap
*   **Purpose:** Show momentum and vision.
*   **Headline:** What's next for Kortex.
*   **Copy direction:** Concise list of upcoming features (Cross-encoder reranking, RLHF).
*   **Visual idea:** A minimalist timeline with glowing current-status markers.

### 14. Documentation
*   **Purpose:** Provide immediate technical depth.
*   **Headline:** Dive deep into the docs.
*   **Copy direction:** "Read the complete architecture spec and API reference."
*   **Visual idea:** A card resembling a sleek book or manual with a link arrow.

### 15. FAQ
*   **Purpose:** Overcome objections.
*   **Headline:** Questions, answered.
*   **Copy direction:** Clear, honest answers to common technical and business questions.
*   **Visual idea:** Simple, elegant accordion menus.

### 16. CTA
*   **Purpose:** Final push to convert.
*   **Headline:** Ready to unlock your enterprise knowledge?
*   **Copy direction:** Clear next steps: Talk to sales or read the docs.
*   **Visual idea:** A large, dark card with a prominent, glowing primary button.

### 17. Footer
*   **Purpose:** Navigation and compliance.
*   **Headline:** N/A
*   **Copy direction:** Links to GitHub, Docs, Pricing, Privacy, Terms.
*   **Visual idea:** Clean, organized multi-column layout.

---

## PART 3: HERO SECTION

**Small announcement badge:** `Introducing Kortex 1.0 — The zero-leak enterprise RAG platform →`
**Headline:** Intelligence you can trust. Access you can control.
**Supporting paragraph:** Unify your fragmented PDFs, databases, and logs into a single, intelligent graph. Kortex enforces strict role-based access control inside the retrieval engine, delivering perfectly cited answers with zero hallucinations and zero data leaks.
**Primary CTA:** View Documentation
**Secondary CTA:** Request Enterprise Demo
**Background illustration ideas:** A deep space/dark mode background with a subtle, glowing mesh gradient. A constellation of nodes representing data sources slowly connecting.
**Animation ideas:** As the user scrolls, the nodes snap into an organized grid, symbolizing Kortex structuring chaotic data.
**Mockup ideas:** A sleek, semi-transparent terminal window layered over the background, automatically typing a query: `> kortex query "Show finance budget allocations" --role Finance`. The answer streams in below with glowing citations.

---

## PART 4: FEATURE CARDS (Bento Grid)

1.  **Hybrid Retrieval Engine**
    *   **Description:** Min-max fused dense vectors and BM25 sparse search.
    *   **Business value:** Finds exactly what you need, even obscure product codes or acronyms.
    *   **Technical value:** Overcomes the limitations of pure vector search by anchoring exact identifiers.
    *   **Suggested icon:** `Search` / `Layers`
    *   **Visual idea:** An animated equalizer showing two signals merging into one.

2.  **Defence-in-Depth RBAC**
    *   **Description:** Strict, document-level role-based access control.
    *   **Business value:** Complete compliance. Zero risk of cross-department data leakage.
    *   **Technical value:** RBAC is applied as a vector pre-filter and a full per-result check before fusion.
    *   **Suggested icon:** `ShieldCheck`
    *   **Visual idea:** A layered shield that glows green as a document passes through it.

3.  **Verifiable Citations**
    *   **Description:** Every answer is grounded with exact document and snippet links.
    *   **Business value:** Ends hallucinations. Users can trust and verify every claim.
    *   **Technical value:** Extractive grounding forces the LLM to cite-or-refuse based only on retrieved context.
    *   **Suggested icon:** `Link` / `Quote`
    *   **Visual idea:** Text highlighting sequentially with numbered `[1]` badges appearing.

4.  **Heterogeneous Ingestion**
    *   **Description:** Unified processing for PDFs, CSVs, SQL, and JSON logs.
    *   **Business value:** Breaks down silos. One search bar for the entire company.
    *   **Technical value:** A common `RawDocument` model maps everything into one single fused index.
    *   **Suggested icon:** `Database` / `FileText`
    *   **Visual idea:** Different file format icons flying into a central, glowing cube.

5.  **Offline-First Resilience**
    *   **Description:** Runs entirely offline with graceful fallbacks.
    *   **Business value:** Guaranteed uptime and absolute data privacy (no cloud APIs required).
    *   **Technical value:** Automatic fallback to deterministic hashing and in-memory stores if models fail.
    *   **Suggested icon:** `WifiOff` / `Server`
    *   **Visual idea:** A pulsing server icon wrapped in a protective ring, independent of the cloud.

6.  **Intent Routing**
    *   **Description:** Transparent classifier boosts relevant departments automatically.
    *   **Business value:** Faster, more accurate answers without user configuration.
    *   **Technical value:** Classifies intent (lookup/summarize/list) and routes via keyword signal prior to vector search.
    *   **Suggested icon:** `GitMerge` / `Route`
    *   **Visual idea:** A glowing dot traveling down a branching path, picking the optimal route.

7.  **Comprehensive Audit Trail**
    *   **Description:** Every access decision and generation is logged and explainable.
    *   **Business value:** Audit readiness and transparent governance.
    *   **Technical value:** `/audit` endpoint exposes routing rationale and allow/deny reasons.
    *   **Suggested icon:** `List` / `Activity`
    *   **Visual idea:** A sleek, scrolling log of green "ALLOW" and red "DENY" JSON objects.

8.  **Developer-Ready**
    *   **Description:** Deploys instantly via Docker, with a typed FastAPI backend.
    *   **Business value:** Low implementation cost and fast time-to-value.
    *   **Technical value:** CI/CD ready, twelve-factor app architecture, comprehensive test suite.
    *   **Suggested icon:** `Terminal` / `Code`
    *   **Visual idea:** A glowing command prompt typing `docker-compose up -d`.

---

## PART 5: VISUAL DESIGN

*   **Typography:** Inter (San Francisco-esque, highly legible) for UI elements. JetBrains Mono for code blocks and technical data. Geist or similar geometric sans-serif for massive headlines.
*   **Spacing system:** 8pt grid system. Generous padding inside cards (32px or 48px) to let content breathe.
*   **Color palette:**
    *   Background: Deep Space Black (`#050505`) to dark charcoal (`#111`).
    *   Primary Accent: Vercel-style high-contrast White (`#FFFFFF`).
    *   Secondary Accent: Electric Blue (`#0070F3`) or a subtle Indigo/Purple gradient for AI elements.
    *   Success: Emerald Green (`#10B981`) for RBAC success/citations.
    *   Danger: Rose Red (`#F43F5E`) for RBAC denial.
*   **Gradients:** Subtle, dark-to-transparent meshes behind key sections. Avoid harsh, solid gradients. Think "glow" rather than "paint".
*   **Shadows:** In dark mode, use colored, diffuse glows instead of drop shadows.
*   **Card design:** 1px subtle borders (`rgba(255,255,255,0.1)`), deep dark backgrounds, and a slight glassmorphic blur if content scrolls underneath.
*   **Button design:**
    *   Primary: Solid white background, black text. High contrast, sharp edges (2px-4px radius).
    *   Secondary: Transparent, 1px white border, white text. Hover states invert or glow.
*   **Animations:** Smooth, low-friction. 300ms ease-out for hovers. Subtle spring physics for expanding elements.
*   **Glass effects:** Used sparingly for sticky navigation and overlaid modal windows.
*   **Dark mode:** Default and primary identity.
*   **Light mode:** Supported for accessibility, using clean whites, subtle gray borders (`#EAEAEA`), and pitch-black text.

---

## PART 6: UI COMPONENTS

*   **shadcn/ui:** Perfect for base components (buttons, inputs, dialogs). It’s unstyled by default, allowing us to enforce our strict, Vercel-like aesthetic without fighting framework defaults.
*   **Magic UI:** Excellent for the hero section background (e.g., animated grid or beam effects) and the bento box grid layout. Brings the "Linear" feel.
*   **Aceternity UI:** We will use this for the complex, attention-grabbing components like the "Architecture" pipeline visualization or the "How it works" scroll-sequence. It excels at technical storytelling.
*   **21st.dev:** Good for sourcing high-quality, complex Tailwind layouts quickly.
*   **Framer Motion:** The backbone of all animations. Essential for the smooth, physical feel of the UI (spring animations on card hover, orchestrating the pipeline animation).
*   **Tailwind components:** Utility-first CSS ensures absolute consistency in our 8pt grid and color tokens.
*   **Lucide icons:** Clean, consistent, and professional line icons. Perfect for the technical, unpretentious vibe.

---

## PART 7: USER JOURNEY

### Recruiter (10s) -> Engineer (30s) -> CTO (2m) -> Founder/Investor (2m+)

*   **Recruiter (10s):** They scan the hero. They see "Secure Enterprise RAG" and a professional, Linear-like design. They understand this is a serious B2B tool, not a toy. They look for the "Careers" or "About" page.
*   **Engineer (30s):** They scroll past the hero straight to the "Architecture" and "Developer Experience" sections. They see the code block (`docker-compose up`), notice the offline-first mention, and appreciate the lack of marketing fluff. They understand they can run this locally without API keys.
*   **CTO (2m):** They read the "Problem" and "Solution" sections carefully. The phrase "Defence-in-Depth RBAC" catches their eye. They read the "Security" section and understand that access control is enforced *before* the LLM sees the data. They see the architecture diagram and trust the technical foundation.
*   **Founder / Investor (2m):** They look at the "Features" (Bento grid) and "Use Cases". They see the broad applicability across HR, Finance, and Engineering. They understand the massive market potential of solving the enterprise data silo problem securely. They check the "Social Proof" (GitHub stars) and click the CTA to request a demo or view the repo.

---

## PART 8: CONTENT STRATEGY

*   **Section headlines:**
    *   *Hero:* Intelligence you can trust. Access you can control.
    *   *Security:* Governing the retrieval path.
    *   *Performance:* Fused hybrid search. Millisecond latency.
*   **Micro-copy:** "Zero hallucinations." "Offline capable." "Document-level ACLs."
*   **Button text:** "Read the Specs", "Deploy Locally", "View on GitHub", "Request Demo".
*   **Feature titles:** Hybrid Fusion, Deep RBAC, Extractive Grounding, Universal Ingestion.
*   **Call-to-actions:** "Start building securely." "See the source."
*   **Marketing copy:** "The knowledge you need, with the security you demand."
*   **Technical copy:** "Min-max normalized dense vectors combined with BM25 sparse search." "Enforced via dual-layer vector pre-filtering and explicit document ACLs."

*   **Rule:** Be human. Be direct. No "synergistic AI paradigms". Just "Grounded answers. Governed access."

---

## PART 9: SOCIAL PROOF

*   **Metrics:** "28 Passing Tests", "Zero Cross-Department Leakage", "100% Offline Capable".
*   **Benchmarks:** "Retrieval in < 50ms", "0% Hallucination on Extractive Mode".
*   **Badges:** "SOC2 Ready" (Conceptual), "Open Source".
*   **GitHub stars section:** A prominent, real-time counter of GitHub stars and forks, emphasizing community trust and open engineering.
*   **Technology logos:** "Built with" section: FastAPI, ChromaDB, Python, Docker.
*   **Enterprise trust indicators:** "Designed for Finance, Healthcare, and Defense."
*   **Testimonials (structure only):**
    *   *Quote:* "A concise statement about how Kortex solved a specific security or silo problem."
    *   *Name, Title*
    *   *Company Logo* (Monochrome)

---

## PART 10: ASSETS TO CREATE

*   [ ] **Dashboard screenshots:** High-fidelity UI mockups of a web interface (even if it's currently a CLI/API, we are designing the *product vision*).
*   [ ] **GIFs:** Animated sequences of the CLI demo running perfectly.
*   [ ] **CLI demos:** Asciinema recordings of the `run_demo.py` script.
*   [ ] **Architecture diagrams:** Clean, sleek redraws of `diagrams/architecture.mmd` matching the new dark-mode brand style.
*   [ ] **Workflow diagrams:** A visual representation of the RBAC enforcement flow.
*   [ ] **Animated SVGs:** The pipeline steps glowing in sequence.
*   [ ] **Icons:** Custom, crisp SVG icons for the Bento grid.
*   [ ] **OpenGraph image:** A stunning 1200x630 image with the logo, tagline, and a subtle code background for social sharing.
*   [ ] **Logo:** "Kortex" - A minimalist geometric mark (e.g., a node connecting securely to a block).
*   [ ] **Favicon:** The geometric mark, optimized for 16x16 and 32x32.

---

## PART 11: DESIGN SYSTEM

*   **Color tokens:**
    *   `--bg-primary: #050505`
    *   `--bg-secondary: #111111`
    *   `--text-primary: #FFFFFF`
    *   `--text-secondary: #888888`
    *   `--accent: #EAEAEA`
    *   `--success: #10B981`
    *   `--danger: #F43F5E`
*   **Border radius:**
    *   `--radius-sm: 4px` (buttons, small inputs)
    *   `--radius-md: 8px` (cards)
    *   `--radius-lg: 12px` (large layout containers)
*   **Spacing:** `4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px`.
*   **Typography scale:**
    *   Display: 72px / -2% tracking
    *   H1: 48px / -1% tracking
    *   H2: 36px
    *   H3: 24px
    *   Body: 16px / 150% line height
    *   Code: 14px / JetBrains Mono
*   **Grid:** 12-column fluid grid.
*   **Container widths:** Max width 1200px.
*   **Responsive breakpoints:** Mobile (<768px), Tablet (768px - 1024px), Desktop (>1024px).
*   **Animation timings:** Base transition: `200ms ease-out`. Complex sequences: orchestrated via Framer Motion with subtle spring physics (e.g., `stiffness: 100, damping: 20`).

---

## PART 12: OUTPUT

### Complete Sitemap
1.  `/` (Home / Landing)
2.  `/docs` (Documentation Hub)
3.  `/docs/architecture` (Deep Dive)
4.  `/docs/security` (RBAC & Compliance)
5.  `/github` (External Link)

### Complete Landing Page Outline
1. Navigation (Sticky, glassmorphic)
2. Hero (Headline, CTAs, Terminal Mockup)
3. Social Proof (Logos/Stars)
4. Problem Statement (Siloed vs. Unified)
5. Solution Overview (Architecture visual)
6. Feature Bento Grid (8 Cards)
7. Security Deep Dive (RBAC explanation)
8. Developer Experience (Code snippet)
9. FAQ (Accordion)
10. Final CTA
11. Footer

### Component Hierarchy
*   `Layout`
    *   `Navbar`
    *   `HeroSection`
        *   `AnimatedTerminal`
    *   `LogoTicker`
    *   `ProblemSection`
    *   `ArchitectureSection`
        *   `PipelineDiagram`
    *   `BentoGrid`
        *   `FeatureCard` (x8)
    *   `CodeSection`
        *   `SyntaxHighlighter`
    *   `FAQAccordion`
    *   `Footer`

### Section Hierarchy
H1 > Subtitle > Primary CTA > Secondary CTA > H2 (Section Title) > H3 (Feature Title) > Body Text.

### Wireframe Description
A single-column, long-scrolling page. Dark theme throughout. Ample negative space between sections (128px). Use of subtle, glowing borders to define content areas rather than solid backgrounds. Text is center-aligned for major headers, left-aligned for detailed prose.

### Design System
(See Part 11)

### Brand Guide
(See Part 1)

### Animation Plan
1. On load: Hero text staggers in (fade + slight upward translation). Terminal mockup types out query automatically.
2. On scroll (Problem): The "chaos" side of the graphic shakes slightly, the "Kortex" side flows smoothly.
3. On scroll (Bento): Cards stagger fade-in. Hovering a card triggers a slight scale (`1.02`), brightens the border, and triggers an inner micro-animation (e.g., the shield icon glows).
4. On scroll (Architecture): The pipeline steps light up sequentially from left to right as they enter the viewport.

### Asset Checklist
(See Part 10)

### Developer Handoff Checklist
*   [ ] Figma file with defined design tokens (colors, typography, spacing).
*   [ ] Exported SVG assets (icons, diagrams).
*   [ ] Asciinema JSON recordings for terminal animations.
*   [ ] Copy deck in Markdown format.
*   [ ] Next.js + Tailwind + shadcn/ui project skeleton initialized.
*   [ ] Framer Motion variants defined in code.
