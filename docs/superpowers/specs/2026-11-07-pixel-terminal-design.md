# X-RUSH // OUT OF BOUNDS — Profile Design

## Intent

Redesign the GitHub profile as a refined pixel-art developer console: distinctive, technical and playful without becoming a rough 8-bit template. The personal signature is the existing idea of being an intentional `INDEX_OUT_OF_BOUNDS` exception and one developer shipping like a full party.

## Goals

- Make the first screen recognizably X-RUSH through a custom pixel scene, not a generic typing widget.
- Preserve the real bilingual project content and every existing project link.
- Turn the four product lines into a party/loadout metaphor and projects into active quests.
- Keep all **39 technology badges**, fully expanded, and make their quantity feel like a complete inventory.
- Use crisp pixel geometry with restrained glow, readable typography and subtle motion.

## Non-goals

- Do not create an independent portfolio website.
- Do not add JavaScript to the GitHub profile or depend on custom page CSS.
- Do not remove, collapse or shorten the technology inventory.
- Do not change project descriptions into unverified claims or add new projects.
- Do not use continuous full-screen glitch, flashing, sound or heavy animation.

## Anti-goals

This fails if it looks like a generic neon cyberpunk template, sacrifices readability for pixel fonts, breaks mobile layout, loses existing content, or turns the badge collection into a cluttered mismatch of sizes.

## Visual System

- Canvas: `1280 × 420` hero with a dark terminal chassis.
- Background: `#070A12`; panels: `#0D1321`.
- Primary: electric cyan `#5DEFFF`; secondary: exception violet `#9D7CFF`.
- Status: acid green `#B8F35A`; intentional exception accents may retain orange `#FF6B35`.
- Body text: `#D7E1EA`; secondary text must remain legible against the dark canvas.
- Pixel artwork uses square steps and `crispEdges`; soft glow is confined to small accents.
- Pixel lettering belongs in the artwork. README body copy remains normal GitHub text.
- Motion is limited to cursor blinking, small particle drift and a subtle pixel core. All CSS animation has a `prefers-reduced-motion` static fallback; do not use uncontrolled SMIL animation.

## Page Structure

1. **Hero** — a responsive `<picture>` using local `assets/banner.svg` on desktop and `assets/banner-mobile.svg` at widths up to 640px; X-RUSH, `ONE DEVELOPER. FULL PARTY.`, product lines and an out-of-bounds pixel entity. The mobile composition is `640 × 640` with all SVG text at least 18px before scaling.
2. **01 / WHOAMI** — compact terminal identity, mission and motto.
3. **02 / PARTY MEMBERS** — four slots: ENGINEER, ARCHITECT, BUILDER, SCOUT, mapped to engines, workflows, apps and content.
4. **03 / ACTIVE QUESTS** — existing draftdesk, app-dev-workflow and photo-retouch links and bilingual descriptions, with custom pixel icons.
5. **04 / FORGE SYSTEM** — existing image-forge, music-forge and video-forge links and bilingual descriptions, presented as one connected engine family.
6. **05 / INVENTORY** — all 39 existing badges in the existing six categories, fully visible. Category labels use slot numbers and counts. Badge sources retain `for-the-badge` height; local badge SVGs remain 28px high.
7. **06 / SYSTEM METRICS** — GitHub stats and top languages with light/dark variants. The original stats provider returned HTTP 503 during implementation, so use the verified summary-card provider with `tokyonight` in dark mode and `default` in light mode. The dark `#70a5fd` headings on `#1a1b27` provide approximately 6.90:1 contrast.
8. **07 / CURRENTLY** — preserve all four current venture lines.
9. **Footer** — responsive local pixel footer using `assets/footer.svg` on desktop and the large-type `640 × 240` `assets/footer-mobile.svg` at widths up to 640px, plus build status and follow link.

## Assets

- Modify `assets/banner.svg`.
- Create `assets/footer.svg`.
- Create `assets/banner-mobile.svg` and `assets/footer-mobile.svg` as static, large-type narrow-screen variants.
- Create six self-contained pixel icons under `assets/icons/`: `draftdesk.svg`, `app-dev-workflow.svg`, `photo-retouch.svg`, `image-forge.svg`, `music-forge.svg`, `video-forge.svg`.
- Existing local badge files stay in use. No external icon font or remote pixel asset is required.

## Accessibility and Robustness

- Every informative image has meaningful alternative text; every SVG has `role="img"` and an accessible name.
- Project links remain ordinary readable links outside the artwork.
- The dark hero must work on both GitHub light and dark page themes; stats retain explicit light/dark variants.
- SVGs contain no scripts, event handlers, external font imports or external image dependencies.
- README tables must wrap naturally on narrow screens; do not use fixed-width full-page containers.

## Acceptance

- All 39 original technology names occur exactly once in the inventory.
- All six original project links and four current ventures remain.
- All local image references resolve and all SVGs parse as XML.
- No typing-widget or capsule-wave template dependency remains.
- Headless Chromium renders the hero without errors, and a visual inspection confirms crisp geometry, readable copy and balanced spacing.
