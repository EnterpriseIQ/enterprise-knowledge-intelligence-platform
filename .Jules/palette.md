## 2026-06-23 - [Missing Accessible Names on Icon Links]
**Learning:** Icon-only links (like GitHub links in navigation/footer) without `aria-label` attributes are completely invisible or unintelligible to screen readers, degrading accessibility.
**Action:** Always verify that interactive elements containing only SVGs or icons have an explicit `aria-label` and adequate `focus-visible` states for keyboard navigation.
