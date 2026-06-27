# Visual Assets Plan: EnterpriseIQ

To elevate EnterpriseIQ to a world-class standard (comparable to OpenAI, Vercel, Linear), our visual assets must exude extreme professionalism, technical precision, and minimalist elegance. Below is the comprehensive production asset plan.

## 1. Core Brand Assets

*   **Logo:** A minimalist, geometric monogram (e.g., an intertwined 'E' and 'Q' forming a nodal network or brain structure). Monochrome (black/white) and a primary brand color (e.g., a deep, electric blue or Vercel-esque indigo).
*   **App Icon:** An optimized version of the logo for favicon (`.ico`, `.png`, `.svg` at 16x16, 32x32, 64x64, 180x180 for Apple Touch) and a rounded-square version for potential mobile/PWA deployment.
*   **Typography System:** Inter or Geist (Vercel's font) for primary UI. Fira Code or JetBrains Mono for all code blocks and terminal interfaces.

## 2. Marketing & Social Assets

*   **Hero Image (`hero-dark.png` / `hero-light.png`):** A high-resolution, slightly abstracted 3D render or sleek isometric vector illustration showing a glowing data pipeline feeding into a secure "vault" (representing RBAC and offline execution), then emerging as a clean, structured output.
*   **OpenGraph Image (`og-image.png`):** 1200x630px. Deep dark gradient background, the EnterpriseIQ logo centered, and the text "The Enterprise Knowledge Intelligence Platform" in a bold, high-contrast sans-serif.
*   **Twitter Card (`twitter-card.png`):** Similar to the OG image but optimized for 1024x512px.
*   **Social Preview Images:** Dynamic, auto-generated preview images for individual documentation pages showing the title of the doc and a relevant icon.

## 3. Product & Technical Illustrations

*   **Feature Illustrations (SVG):**
    *   *Hybrid Search:* An abstract visual showing two distinct data streams (dense vectors and sparse keywords) merging into a highly precise target.
    *   *Zero-Trust RBAC:* A multi-layered shield or gateway graphic where only specific data chunks pass through based on a user's badge/key.
    *   *Agentic Workflows:* A nodal graph showing multiple agents (represented by small glowing orbs) collaborating and passing context between each other.
*   **Architecture Diagrams:** (See `DIAGRAMS.md` for Mermaid equivalents, but we need high-fidelity SVG versions designed in Figma or Excalidraw).
    *   *System Architecture:* High-level overview of Ingestion -> Storage -> Retrieval -> Generation.
    *   *Deployment Architecture:* VPC/Air-gapped deployment diagram showing isolated Docker containers and internal networks.
*   **Background Textures:** Very subtle, low-opacity dot-matrix grids, topographical lines, or radial gradients to give depth to landing page sections without distracting from content.

## 4. UI/UX Assets

*   **Dashboard Screenshots:** (See `SCREENSHOTS.md` for exact specs). We need 4K resolution, borderless window screenshots of the platform with dummy enterprise data (e.g., "Acme Corp Financials").
*   **CLI Screenshots:** Clean, high-res screenshots of the terminal output (using a modern terminal emulator like Warp or Ghostty with a custom, sleek theme).
*   **Loading Animations (`.json` Lottie or pure CSS/Framer Motion):**
    *   *Global Loader:* A subtle, pulsing nodal network or spinning geometric shape.
    *   *Query Processing:* A multi-step skeleton loader that visually indicates the current stage (e.g., "Retrieving chunks...", "Applying RBAC...", "Reranking...", "Generating...").
*   **Animated GIFs / WebM:**
    *   *GitHub README Demo:* A fast-paced, 15-second loop showing a terminal query being instantly answered with citations.
    *   *Landing Page Feature Demos:* Small, looping micro-interactions showing the hybrid search in action or the RBAC filter dropping unauthorized chunks.

## Asset Delivery Requirements
*   All static vectors must be delivered as clean, minified SVGs.
*   All static rasters must be WebP format for optimal performance (fallback to PNG).
*   All animations should be WebM or MP4 (h264) with `playsinline loop muted` attributes for the web, falling back to optimized GIFs for GitHub READMEs.