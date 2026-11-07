# Terminal Unification — Profile Body Pass

Date: 2026-11-08
Status: implemented

## Problem

The 1280×420 pixel-console banner established a hard visual language — pixel art, cyan/violet accent, monospace terminal chrome. Everything below it spoke a different language: bilingual tables with `EN · 中文` headers, a rainbow of brand-coloured Shields badges, and generic `---` rules. The hero and the body read as two different pages.

## The single rule

> **English is output. Chinese is a `#` comment.**

Every Chinese sentence on the page is introduced by `#`, exactly as a shell transcript annotates a command. No Chinese appears as prose, as a table header, or as a trailing label. `tests/test_profile.py::test_chinese_is_only_rendered_as_terminal_comments` enforces this and will fail on any line where Chinese arrives without a preceding `#`.

## Structure

Each section is one terminal pane that opens with a prompt line:

```bash
rush@github:~$ <command>
<output lines, English only>
# <中文注释>
```

| Section | Prompt |
|---|---|
| 01 / WHOAMI | `whoami`, `cat mission.txt`, `echo "$EXCEPTION"`, `uptime` |
| 02 / PARTY MEMBERS | `./party --roster` |
| 03 / ACTIVE QUESTS | `quest --active` |
| 04 / FORGE SYSTEM | `forge --status` (ASCII signal diagram) |
| 05 / INVENTORY | `lsmod \| wc -l` → `39` |
| 06 / SYSTEM METRICS | `gh stats --user x-rush` |
| 07 / CURRENTLY | `ps aux \| grep now` |

Structural entries that need links or icons stay as HTML: an icon plus a row of inline `<code>` lines (`> loadout = …` for output, `# …` for the Chinese comment). Tables are gone — `test_body_stays_a_terminal_transcript` fails the build if `<table>`, pipe tables, or a duplicated quest id reappear.

## Mobile is a hard constraint, not a nicety

Trailing comments were the first design and they failed: a code block does not wrap, so on a 390px screen the `# 中文` sat behind a horizontal scrollbar and became invisible — the entire point of the page disappeared on phones. Chinese comments therefore always occupy their own line, and `test_terminal_panes_fit_a_narrow_screen` caps any fenced line at 46 display columns (CJK counted as two).

## Palette

39 badges, one plate colour (`#0D1321`), one logo ink (`#5DEFFF`), white label text, `for-the-badge` throughout — an ANSI-coloured loadout grid instead of a rainbow. The three locally hosted badges (TanStack, Tauri, Aliyun) were recoloured to match while keeping their Shields geometry byte-for-byte (28px height, original widths). Count stays at 39 and stays fully expanded; `test_inventory_badges_share_one_dark_terminal_palette` enforces the ink.

## New artwork

| Asset | Size | Purpose |
|---|---|---|
| `assets/sprites/{engineer,architect,builder,scout}.svg` | 40×40 | 15×15 pixel class sprites, generated |
| `assets/divider.svg` | 880×20 | pixel rule replacing `---`: stair brackets, dashed rail, cyan core |

`tools/gen_pixel_assets.py` generates both families from integer-grid predicates, merging same-colour pixels into horizontal runs so every edge lands on a whole pixel and stays crisp at 1:1.

## Deliberate trade-offs

- Section headings remain Markdown `h2` in the system sans-serif: GitHub owns heading typography, and losing real headings would cost anchors and screen-reader structure.
- Bash panes have empty space to the right on desktop once comments move to their own lines. Mobile legibility wins.
- Dividers are decorative images (`alt="" aria-hidden="true"`); the semantic section break is still the heading.
- Real syntax highlighting only exists on github.com, so the local preview shows comments in body colour; the live page greys them correctly.
