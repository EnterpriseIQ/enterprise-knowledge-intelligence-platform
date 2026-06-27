# EnterpriseIQ: Pre-Launch Production Checklist

This checklist must be fully resolved before announcing EnterpriseIQ 2.0 to the public, ProductHunt, or HackerNews.

## Phase 1: Code & Performance Freeze
- [x] **Backend Tests:** Run `python -m pytest` and ensure 100% pass rate.
- [x] **Frontend Build:** Verify `pnpm build` completes without errors and bundle size is optimized.
- [x] **Linting:** Ensure `ruff check` and `pnpm lint` return zero warnings.
- [x] **Security Audit:** Verify no hardcoded secrets exist in the repository.
- [x] **CORS:** Ensure `src/api/main.py` has a secure and functional CORS configuration.
- [x] **Accessibility:** Verify all custom UI components (Accordions, Modals) have WAI-ARIA roles and `focus-visible` states.
- [x] **SEO:** Ensure `website/index.html` has complete OpenGraph and Twitter meta tags.

## Phase 2: Documentation & Assets
- [ ] **Visual Assets:** Generate and compress all assets listed in `VISUAL_ASSETS_PLAN.md`.
- [ ] **Screenshots:** Capture high-fidelity screenshots as specified in `SCREENSHOTS.md`.
- [ ] **Demo Videos:** Record and edit the 3-minute and 10-minute demos (`PRODUCT_DEMOS.md`).
- [ ] **Diagrams:** Render the Mermaid code in `DIAGRAMS.md` into SVGs for the README and website.
- [x] **Code Docstrings:** Ensure all core pipeline methods have comprehensive Google-style docstrings.

## Phase 3: Deployment & Infrastructure
- [ ] **Docker Registry:** Push the final `enterpriseiq-backend` and `enterpriseiq-frontend` images to Docker Hub or GHCR.
- [ ] **GitHub Pages:** Verify the `.github/workflows/deploy-pages.yml` pipeline successfully deploys the frontend dashboard.
- [ ] **Vite Base Path:** Confirm `vite.config.ts` matches the GitHub repository name (`/enterprise-knowledge-intelligence-platform/`).
- [ ] **Load Testing:** Run a basic load test against the API to ensure the local ChromaDB and SQLite instances don't lock under concurrent load.

## Phase 4: Launch Day Logistics
- [ ] **Release Notes:** Draft a highly detailed `RELEASE.md` outlining the architectural shift to Agentic RAG and the new UI.
- [ ] **Social Copy:** Prepare LinkedIn and Twitter threads highlighting the "Why" (Hallucination prevention + RBAC).
- [ ] **Community Monitoring:** Assign team members to monitor GitHub Issues and Discussions for the first 48 hours post-launch.