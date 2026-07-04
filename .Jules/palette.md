## 2024-11-20 - [Accessibility in Framer Motion Components]
**Learning:** In this project, interactive UI elements built with Framer Motion components (like `AnimatePresence` and `<motion.div>` in the FAQ accordion) lack native ARIA attributes by default. Relying on them out of the box causes accessibility gaps for screen readers.
**Action:** When creating or modifying interactable Framer Motion components (e.g., accordions, modals), explicitly add WAI-ARIA roles (e.g., `role="region"`), state attributes (e.g., `aria-expanded`, `aria-controls`), and corresponding IDs to link them. Additionally, ensure keyboard focus states (`focus-visible` utilities) are manually added so keyboard users can navigate these custom elements.

## 2024-07-04 - [Accessibility Keyboard Focus in Suggested Queries]
**Learning:** In the `QueryForm.tsx` component, interactive elements like the "Suggested Queries" and "History" buttons lacked visual focus indicators when navigating via keyboard, making it difficult for keyboard-only users to see which element is active.
**Action:** Explicitly added Tailwind CSS `focus-visible` utility classes (`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background`) to these interactive buttons to ensure accessibility standards are met and a premium UX is maintained for all users.
