# X-RUSH Pixel Terminal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the GitHub profile as a refined, animated pixel terminal while preserving all projects, bilingual content and all 39 technology badges.

**Architecture:** The deliverable remains a GitHub Profile README with sanitized HTML and local SVG assets. Custom artwork supplies the visual identity; Markdown supplies readable, linkable content. Standard-library Python tests pin content and SVG contracts, while headless Chromium supplies visual verification.

**Tech Stack:** Markdown, inline HTML, self-contained SVG/CSS, Python `unittest`, headless Microsoft Edge.

**Spec:** `docs/superpowers/specs/2026-11-07-pixel-terminal-design.md`

## Global Constraints

- Keep the deliverable inside `x-rush/x-rush`; do not build a separate website.
- Keep all 39 badges fully expanded in six categories and all existing project links and current ventures.
- Hero canvas is exactly `1280 × 420`; use `#070A12`, `#0D1321`, `#5DEFFF`, `#9D7CFF`, `#B8F35A` and `#D7E1EA`.
- No JavaScript, remote fonts, external icon dependencies, uncontrolled SMIL animation or missing reduced-motion fallback.
- Every image has alternative text and every SVG has an accessible name.
- Do not push or alter the public GitHub repository without separate explicit approval.

## Review Focus

- **Mobile tables:** long bilingual descriptions and badge rows must wrap rather than force a fixed page width. Task 2 checks that no fixed-width page container is introduced; Task 3 inspects a 390px render.
- **Lost badges during rewriting:** all 39 names must appear exactly once. Task 2 pins the exact expected name set and count.
- **Unreadable neon/glow:** body text and project links must remain crisp. Task 1 rejects SVG filter elements in favor of layered geometry; Task 3 visually checks both desktop and mobile renders.
- **Animation ignoring reduced motion:** Task 1 requires CSS-only animation plus an explicit reduced-motion override and rejects SMIL elements.
- **Broken local assets on GitHub:** Task 2 resolves every local `img src` and `source srcset` relative to the repository root.

---

### Task 1: Pixel Artwork and Asset Contract

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_profile.py`
- Modify: `assets/banner.svg`
- Create: `assets/footer.svg`
- Create: `assets/icons/{draftdesk,app-dev-workflow,photo-retouch,image-forge,music-forge,video-forge}.svg`

**Interfaces:**
- Consumes: the visual system and asset names fixed by the spec.
- Produces: local SVGs referenced by `README.md`; `python -m unittest tests.test_profile -v` for repeatable validation.

- [ ] **Step 1: Write failing asset tests**

Create tests that parse SVG XML and assert: the banner viewBox is `0 0 1280 420`; required palette tokens occur; pixel geometry uses `crispEdges`; CSS contains `prefers-reduced-motion` and disables animation; no SVG contains `script`, `filter`, event handlers, external resource references or SMIL `animate` elements; every SVG has `role="img"` and `aria-label` or a `<title>`.

- [ ] **Step 2: Run asset tests and verify failure**

Run: `python -m unittest tests.test_profile.ProfileAssetTests -v`
Expected: FAIL because the old banner is `1200 × 420`, uses SMIL, and the new footer/icons do not exist.

- [ ] **Step 3: Build the pixel artwork**

Replace the hero with the approved terminal/out-of-bounds composition. Use vector rectangles and paths for pixel text/artwork, system monospace only for secondary copy, and CSS keyframes only for small cursor/particle/core motion. Add the six 32px project icons and a wide footer using the same palette and accessible SVG structure.

- [ ] **Step 4: Run asset tests and verify success**

Run: `python -m unittest tests.test_profile.ProfileAssetTests -v`
Expected: PASS for all asset tests.

- [ ] **Step 5: Commit the asset milestone**

```bash
git add docs/superpowers tests assets/banner.svg assets/footer.svg assets/icons
git commit -m "feat: add refined pixel profile artwork"
```

### Task 2: README Recomposition and Complete Inventory

**Files:**
- Modify: `README.md`
- Modify: `tests/test_profile.py`

**Interfaces:**
- Consumes: the eight local SVG assets produced by Task 1 and existing README content.
- Produces: the final seven-section profile with exactly 39 inventory badges.

- [ ] **Step 1: Write failing README tests**

Add tests for all seven headings, the six existing project URLs, four current venture lines, local banner/footer references, and removal of `readme-typing-svg` and `capsule-render`. Parse images with `html.parser`; assert every local reference exists and every image has non-empty alt text. Reject fixed-width page containers and CSS `min-width`/`width:` declarations in the README. Pin the inventory to these 39 unique names: TypeScript, JavaScript, Python, Go, PHP, Java, Rust; React, Next.js, Vue.js, Vite, TanStack, React Native, Tauri, PWA; Express, FastAPI, Spring Boot, Laravel, Gin; MySQL, PostgreSQL, MongoDB, Redis, SQLite; Docker, Kubernetes, Nginx, Linux, Node.js, Git, GitHub Actions, CloudBase, Aliyun; fal.ai, Replicate, ffmpeg, Prompt Engineering, Agent Skills. Assert Shields badges use `style=for-the-badge` and local badge SVGs are 28px high.

- [ ] **Step 2: Run README tests and verify failure**

Run: `python -m unittest tests.test_profile.ProfileReadmeTests -v`
Expected: FAIL on the new section names, local footer and removed template dependencies.

- [ ] **Step 3: Rewrite README without dropping content**

Implement the seven sections in the spec. Use compact terminal copy, the party table, quest/forge tables with the new 32px icons, and the complete badge inventory with numbered category labels and counts. Recolor stats to cyan/violet while retaining light/dark `<picture>` variants. Use no fixed-width page container and no collapsed badge section.

- [ ] **Step 4: Run the complete suite**

Run: `python -m unittest tests.test_profile -v`
Expected: all asset and README tests PASS, including exactly 39 unique inventory badges.

- [ ] **Step 5: Commit the README milestone**

```bash
git add README.md tests/test_profile.py
git commit -m "feat: rebuild profile as pixel developer console"
```

### Task 3: Visual Verification and Delivery

**Files:**
- Modify only if inspection reveals a defect: `README.md`, `assets/banner.svg`, `assets/footer.svg`, `assets/icons/*.svg`
- Create outside the committed source tree: `artifacts/x-rush-banner.png`, `artifacts/x-rush-profile-preview.png`

**Interfaces:**
- Consumes: the final README and local SVGs.
- Produces: verified artwork plus a visual preview for delivery.

- [ ] **Step 1: Render the hero and profile preview**

Use headless Microsoft Edge at desktop width and at 390px mobile width. A temporary local HTML harness may approximate GitHub spacing, but it must reference the real local assets and preserve the README content; it is verification tooling, not another product.

- [ ] **Step 2: Inspect and correct visual defects**

Inspect the PNGs for clipped copy, overflow, blurry pixel edges, excessive glow, mismatched badge sizing and unreadable contrast. Make only targeted corrections required by observed defects.

- [ ] **Step 3: Run final automated and repository checks**

Run: `python -m unittest tests.test_profile -v`
Expected: all tests PASS.
Run: `git diff --check` and `git status --short --branch`.
Expected: no whitespace errors; only intentional changes are present.

- [ ] **Step 4: Commit any verification corrections**

If Step 2 changed source, rerun Step 3 and commit with `fix: polish pixel profile rendering`. Do not commit generated screenshots or temporary preview tooling.
