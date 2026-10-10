# Landscape dashboard design system (v2)

The visual law for every landscape repo's `index.html`. It replaces the v1 "tender comparison sheet" system (fixed grey-green paper, monochrome competitors, no imagery). Everything here is **fixed** unless it is marked **derived**, and derived values are produced by a procedure, never by taste on the day. Copy follows `reference/dashboard-voice.md`; this doc only governs what the words sit in.

Companion files:
- `derive_tokens.py`: turns one brand colour into the complete light and dark token set, contrast-checked. Run it; never hand-pick a hex.
- `assets.py`: implements section 8. `capture` takes the screenshots (consent dismissal, lazy-load scroll, and gates 1, 2 and 4 automated) and collects logo candidates and brand signals; `exhibit` takes crops; `font` fetches the typefaces; `embed` inlines everything. Gates 3 and 5 and the logo choice stay a visual check by the builder.
- `templates/dashboard.html`: the reference implementation (the Turo run). Start from it.
- The per-run block (section 12) is written once per repo as a comment at the top of the CSS and reused on every rebuild.

---

## 1. Who this is for, and the 10-second test

**Reader.** A product or leadership person at the target company who opens a link cold, from a message or a LinkedIn post, usually on a laptop and sometimes on a phone. They didn't ask for it. They are asking themselves two things: does this person understand our business, and is the work real?

**The page's job.** Answer both before the reader scrolls, then reward the reader who does scroll with evidence they can check.

**The 10-second test.** At 1440x900, with no scrolling, the reader must be able to see:
1. That this is independent work by a named person, about their company.
2. The headline finding, stated as a specific sentence.
3. The real market: every competitor's actual homepage and logo, with the ones in trouble visibly marked.
4. How far to trust it: the Observed/Inferred ratio and the re-check date.

Strategy-mode runs (9.2a) replace item 3 with "the answer to each question in the brief".

If a build fails any of the four at the fold, it isn't finished.

## 2. Concept: the frame is the author's, the ink is the target's

Every landscape page is built from two layers, and keeping them apart is what makes the page read as tailored and independent at once.

- **The frame is fixed, and it's the author's.** Layout, grid, type scale, the mono annotation face, exhibit frames, capture captions, encoding textures, the byline. This stays the same across every company, so the series reads as one person's body of work, and so the page never looks like the target's own collateral.
- **The ink is derived, and it's the target's.** One accent from the target's brand colour, neutrals tinted toward that hue, a dark ground borrowed from the brand where it has one, and an open-licence typeface matched to the brand's type. That is what makes a Turo page feel made for Turo.
- **The evidence is theirs too.** Competitor homepages and logos appear as labelled exhibits, in full colour, inside the author's frame. Colour in imagery identifies companies. Colour in data marks is reserved (section 5).

The register is an analyst's briefing with exhibits. Real screenshots do the visual work that v1 tried to get from typography alone.

## 3. Page architecture

**Two tabs: Analysis and Evidence and method.** Reversed on 3 Oct 2026 after the single scroll read as overwhelming on first view. Tab 1 carries the argument and ends on the ask (going broader). Tab 2 carries the evidence and how the page was built. Discovery of tab 2 relies on three routes: the masthead tab, the trust panel's link, and the Next row that ends tab 1. Every anchor deep-links, and the tab follows the hash (spec in 9.1a). Scripts: the theme toggle, the tab router and the drawer (9.24).

Order and anchors:

| # | Section | Tab | Anchor | Content source |
|---|---|---|---|---|
| 0 | Masthead (sticky) | both | | fixed |
| 1 | Hero: eyebrow, headline, standfirst, trust panel, cast strip | Analysis | `#top` | analysis summary, counts, asset manifest |
| 2 | Findings, each paired with at most one exhibit | Analysis | `#findings` | executive summary |
| 3 | The field: a roster grid of player cards, each labelled with its cluster (D6); falls back to clusters, each holding player cards, only when most clusters hold more than one card; in strategy mode, a compact roster (9.11) | Analysis | `#field` | clusters + profiles |
| 4 | Comparison matrix | Analysis | `#compare` | analysis matrix |
| 5 | Where the target stands: strengths, gaps, open ground | Analysis | `#position` | positioning section |
| 6 | Lens deep-dive (optional; only when the analysis has one) | Analysis | `#options` | e.g. "what a sports partnership could look like" |
| 7 | Recommendations (F8: optional, only when the analysis has a ranked recommendations section) | Analysis | `#recommendations` | analysis |
| 8 | Open questions and going broader (F8: when the analysis has no separate open-questions list, it merges into this section instead of running twice), ending with the Next row into tab 2 | Analysis | `#next` | analysis |
| 9 | Evidence: confidence bars, per-profile bars, verification line | Evidence and method | `#evidence` | label counts + verification note |
| 10 | Part 2 opener band | Evidence and method | `#method` | fixed + repo state |
| 11 | Process rail, why this compounds, labelling, material change, trust boundary, limits; ends with a link back to tab 1 | Evidence and method | `#process`, `#compounds`, `#labels`, `#material`, `#trust`, `#limits` | skills + README |
| 12 | Footer and colophon | both | `#colophon` | fixed + per-run block |

Every piece of content the v1 structure covered is still here. Merges: v1's archetype cards and competitor-detail disclosures become section 3 (cards grouped by cluster). v1's confidence bar grows into section 9.

**Cut from v1, on purpose:**
- **Category hues.** Screenshots and logos already bring six or more foreign colours onto the page, so four chart hues on top would make a carnival. The hue-collision fallback was also the most fragile rule in v1. Clusters are now shown by grouping and position.
- **CSS-counter section numbers.** Numbering now appears only where order is real (section 5, rule 8).
- **The ink-density strength grid.** The position board (section 9.13) is easier to read.

## 4. Fixed foundations

- **Traps found on the Turo build.** The phone tab row is a second copy of the nav: the router sets state on both, with `aria-current` on the copy because its links have no `role="tab"`. Chrome blurs focus on fragment navigation, before and after `hashchange`, so the router refocuses the tab in a `requestAnimationFrame`. Panel-start anchors (`#top`, the first section of tab 2) carry `scroll-margin-top` equal to the phone row's height, or every route into a tab lands with the row cut in half under the sticky bar.

### 4.1 Grid and breakpoints

- Content max width `1280px`, centred. Side gutter `clamp(16px, 4vw, 56px)`, set once on the page wrapper with `padding-inline`.
- Desktop (at least 1100px): 12 columns, 24px column gap.
- Tablet (720 to 1099px): 6 columns, 20px gap.
- Phone (under 720px): 4 columns, 16px gap. Nothing may cause horizontal page scroll. Only the matrix, the presence grid and the nav row scroll sideways, each inside its own `overflow-x: auto` container.
- Full-bleed elements (Part 2 opener band only) break out with `margin-inline: calc(50% - 50vw)`.
- **D5. No stretch drift.** Any grid or flex cell that sits in a stretched row and is itself an auto-row grid gets `align-content:start`. Otherwise the spare height spreads between its rows, and labels drift out of line with their neighbours (this happened twice on the first Turo run: the ownership map's children and the figure-pair cells).

### 4.2 Spacing scale

4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 72, 96. No other values.

- Between top-level sections: `padding-block: 96px` desktop, 72 tablet, 56 phone.
- Section heading to section body: 40 desktop, 32 tablet, 24 phone.
- Between sibling blocks inside a section: 24. Between findings: 72.
- Use grid/flex `gap` for sibling spacing, not margins.

### 4.3 Typefaces

Two families per page:
- **Brand match** (derived, section 6.6). Used for display, headings and body. Embedded as base64 `@font-face`, variable weight where available. Token `--font-brand`, with fallback `ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif` (serif matches fall back to `Georgia, serif`).
- **IBM Plex Mono** (fixed, every run; SIL OFL). Used for labels, eyebrows, captions, URLs, dates, commands, figures in tables and chips. Weights 400 and 500. Token `--font-mono`, fallback `ui-monospace, "SF Mono", Menlo, Consolas, monospace`. Plex Mono is the author's constant voice across every target; it is never used for headings or running prose.

### 4.4 Type scale

| Token | Size / line-height | Weight | Tracking | Use |
|---|---|---|---|---|
| `display-xl` | `clamp(38px, 3.2vw + 12px, 60px)` / 1.05 | 750 (700 if the family lacks it) | -0.025em | hero headline only |
| `display-l` | `clamp(32px, 2.4vw + 10px, 46px)` / 1.1 | 700 | -0.02em | Part 2 opener headline |
| `h2` | `clamp(26px, 1.4vw + 14px, 34px)` / 1.18 | 700 | -0.015em | section headlines (sentences), max width 30ch |
| `h3` | 22px / 30px (phone 20/28) | 650 | -0.01em | finding, cluster and recommendation headlines |
| `h4` | 18px / 24px | 650 | -0.005em | card titles, company names in cards |
| `lede` | `clamp(17px, 0.6vw + 13px, 21px)` / 1.5 | 400 | 0 | hero standfirst, Part 2 standfirst, max 58ch |
| `body` | 16px / 26px | 400 | 0 | running text, max 66ch |
| `body-s` | 15px / 24px | 400 | 0 | card summaries, cluster text |
| `small` | 13px / 20px | 400 | 0 | exhibit annotations, fallbacks |
| `label` | 11.5px / 16px, Plex Mono, uppercase | 500 | 0.1em | eyebrows, exhibit labels, row headers |
| `data` | 13px / 20px, Plex Mono | 400 | 0 | figures, URLs, dates, commands; `tabular-nums` |
| `figure` | 44px / 48px, brand face | 700 | -0.02em | E6 figures and the figure strip (9.6a), `tabular-nums` |

Headings take `text-wrap: balance`, paragraphs `text-wrap: pretty`. Bold inside body copy is 600, used at most once per paragraph.

**Type never shrinks to fit; the copy does.** If the hero headline runs past its budget (about 85 characters at `display-xl`, 3 lines at 1440), cut words. Do not step the size down, because that moves the problem onto the hierarchy. The same goes for every other token in the table: an overflowing line is an edit, not a smaller size.

### 4.5 Shape, borders, elevation

- Radii: `--r-s: 4px` (chips, code chips), `--r-m: 8px` (screenshots, small panels), `--r-l: 12px` (cards, exhibit frames). Identity tiles use their own radius (9.4). Nothing else is rounded; text blocks never sit in containers.
- Borders are 1px `--rule` by default and 1px `--rule-strong` for screenshot edges and interactive boundaries. The target's card gets 2px `--accent-fill`.
- No drop shadows anywhere. Separation comes from border, surface step and space.
- Hatch (the Inferred texture), defined once:
  `--hatch: repeating-linear-gradient(135deg, color-mix(in oklab, var(--ink) 34%, transparent) 0 1px, transparent 1px 6px);`
  `--hatch-accent`: the same with `var(--accent-fill) 60%`.

### 4.6 Motion and interaction

- No load animation. The page is fully visible at rest. The one exception is the drawer-in (9.24): 180ms, `cubic-bezier(.2,.7,.2,1)`, written as `@keyframes` and applied to `.drawer[open]` only inside `@media (prefers-reduced-motion: no-preference)`, so reduced motion gets no animation at all. Closing is instant. Do not use `@starting-style`.
- Hover on links and cards: colour and border changes only, `transition: 120ms ease-out`. Removed under `prefers-reduced-motion: reduce`.
- Focus: `outline: 2px solid var(--ink); outline-offset: 2px` on every interactive element. Never removed.
- Links in prose: `--ink` text, 1px underline in `--rule-strong` with 3px offset. On hover the underline turns `--ink`. Links are not accent-coloured, because accent is reserved (section 5).
- Theme toggle: default follows the system. The button stamps `data-theme` on `<html>` and remembers the choice in `localStorage` (inside try/catch). A `?theme=dark` or `?theme=light` query forces a theme on load, for review captures.

## 5. Encoding rules (these carry the page's honesty; never break them)

1. **Accent means the target.** Its card, row, column, marks, chip, and the moves this analysis recommends it make. Nothing else gets accent, including links, nav and focus.
2. **Alert means an ending or restructuring event.** Administration, liquidation, dissolution, market exit, shutdown. Always text plus glyph plus colour, so colour is never the only carrier. Nothing else gets alert.
3. **Observed versus Inferred is texture, never colour.** Texture has a size floor: hatch only reads on a mark at least 6px thick and 24px long (bars, ranges, confidence segments). Anything smaller (dots, rings, cell edges, single-line table cells) carries inference on its text instead: a dotted underline plus a superscript `i`, the same treatment as inline prose. Never try to hatch a 12px glyph or a 4px strip; at 1x they read as a stray chevron. The legend sits above or beside the exhibit, never only in a footer.
4. **Competitors never get a hue in data marks.** Their marks are ink. Their colour lives only inside their logo tile and their screenshot.
5. **Strengths and gaps get no colour.** Glyph and column position carry them.
6. **Judgement axes are ordinal.** Worded end labels, no numbers, no gridlines implying a scale.
7. **Dashed means not done yet.** Survey-depth chips, go-broader cards and "not in market" chips use dashed borders. Full profiles use solid.
8. **Numbers mark real order only.** Findings (ranked), exhibits (referenced by number in the text), recommendations (priority) and process steps (sequence) are numbered. Nothing else is.
9. **Every ratio on the page comes from one count.** Observed/Inferred figures are computed by counting `- Observed:` and `- Inferred` label lines in `profiles/*.md` at build time. The hero, the evidence section and the README must all quote that same count. If prose elsewhere disagrees, the prose is wrong.
10. **Wording is fixed.** "Re-checked against the pages they cite." Never "verified" as a claim about truth.

## 6. Derived per run: brand intake to tokens

### 6.1 Brand signals the capture step supplies

For the target (competitors optional): `theme-color`, chromatic colours from its CSS ranked by frequency, font-family stacks, near-black candidates (OKLCH L 0.12 to 0.22, C under 0.03), and the logo. The target's homepage screenshot is used to confirm by eye.

### 6.2 Picking the brand colour (one colour; the rest are recorded, not used)

In order, take the first that exists:
1. `theme-color`, if chromatic (OKLCH C of 0.04 or more) and not `#FFFFFF`/`#000000`.
2. The most frequent chromatic colour in the site's own CSS, excluding default link blues (`#0000EE`, `#1A0DAB`, `#0645AD`, `#3898EC`, the Webflow default) and colours that only appear in third-party widgets.
3. The dominant chromatic colour of the logo.
4. None: the brand is achromatic, so use neutral mode (6.4).

Then check it against the screenshot. It should be the colour the company uses for its primary action or its mark. If the screenshot contradicts the pick, record why and take the next candidate.

**One accent, even when the brand has more.** Secondary brand colours are recorded in the per-run block and not used. A second brand hue makes the page read as the company's own collateral, and it competes with alert.

### 6.3 The dark ground

If the brand signals include a near-black (L 0.12 to 0.22, C under 0.03) from the target's own CSS, pass it to `derive_tokens.py --dark`. The dark theme then sits on the company's own black. Otherwise the script derives a dark ground at L 0.17 on the brand hue.

### 6.4 Running the derivation

```
python3 derive_tokens.py '<brand hex>' [--dark '<near-black hex>']          # contrast report
python3 derive_tokens.py '<brand hex>' [--dark '<near-black hex>'] --css    # paste-ready token blocks
```

What it does, so a reviewer can check it:
- **Neutrals** keep fixed OKLCH lightness and chroma and borrow only the brand's hue. Every page gets its own tint, and contrast stays identical from run to run. Light ink-3 is at least 4.7:1 on every surface, and dark ink-3 at least 5.9:1.
- **Accent (text).** It starts at the brand colour and moves lightness (darker in light theme, lighter in dark) until it reaches 4.5:1 on `--bg`, `--surface`, `--surface-2` and `--accent-wash`. Hue is kept, and chroma is reduced only to stay in gamut. If the brand already passes, the accent is the exact brand colour.
- **Accent fill** (solid marks: bars, the target card border, chip fill, active markers) is the exact brand colour if it reaches 3:1 on the grounds; otherwise it is stepped until it does. `--on-accent` is white or ink, whichever reads on the fill, and must reach 4.5:1.
- **Wash and line.** `--accent-wash` is a pale tint (light) or deep tint (dark) for the target's column, row and card highlights. Ink and ink-2 stay at 7.5:1 or better on it. `--accent-line` is for decorative rules inside target areas only, never a boundary that has to be seen.
- **Modes**, recorded as `--accent-mode`:
  - `ink`: the normal case. The accent is used as text colour and as fill.
  - `highlighter`: neon or pale brands (lime, yellow, cyan) whose text-safe version would lose its identity (lightness moved more than 0.22, or chroma below 45% of the original). The brand colour then acts only as a fill behind ink: marker behind the headline phrase, chip fill, bar fill, card border. Text "accent" becomes `--ink`. **Every filled accent mark gets a 1px `--ink` outline in this mode**, because the fill itself doesn't reach 3:1 on the ground. Dark theme usually stays in `ink` mode for these brands.
  - `neutral`: achromatic brands (C under 0.04). The accent is `--ink`. The target is marked by a solid ink fill, 700-weight names and the "Subject" label. Neutrals take hue 250 at 60% chroma.
- **Alert** is fixed at hue 28 (red-orange) and stepped to 4.5:1 on every surface and on its own wash. If the brand hue is within 35 degrees of 28 (reds and oranges), alert switches to ink-inverse: `--alert` becomes `--ink` and `--alert-wash` becomes `--surface-2`, and the glyph and text carry the meaning.

Tested cases, with their modes (light / dark): Turo `#593CFB` ink/ink; Spotify-like `#1DB954` ink/ink; Netflix-like `#E50914` ink/ink plus alert clash; lime `#C6FF00` highlighter/ink; yellow `#FFCC00` highlighter/ink; cyan `#00D1FF` highlighter/ink; black `#000000` neutral/neutral. Every text pairing lands at 4.5:1 or better.

### 6.5 Token reference

| Token | Role |
|---|---|
| `--bg` | page ground; `body` background |
| `--surface` | cards, exhibit frames |
| `--surface-2` | caption bars, fallbacks, Part 2 band, code specimens, the "gap" column band |
| `--rule` / `--rule-strong` | hairlines / screenshot edges and interactive boundaries |
| `--ink` / `--ink-2` / `--ink-3` | headings and key text / body / labels and captions |
| `--accent` | target text: labels, first recommendation numeral, headline phrase (ink mode) |
| `--accent-fill` / `--on-accent` | target solid marks / text on them |
| `--accent-wash` / `--accent-line` | target highlight ground / decorative rule inside target areas |
| `--alert` / `--alert-wash` | ending-event chips and markers |
| `--scrim` | the drawer's `::backdrop` and nothing else |

All tokens are declared in bare `:root` first. The dark blocks only redefine them (the script prints all three blocks). `--scrim` follows the same rule but the script does not print it, so add it by hand: bare `:root` gets `color-mix(in oklab, var(--ink) 30%, transparent)`, and both dark blocks (the `prefers-color-scheme` block guarded by `:root:not([data-theme="light"])`, and `:root[data-theme="dark"]`) get `color-mix(in oklab, #000 60%, transparent)`, because `--ink` is light in dark theme and would lighten the page instead of dimming it. Components use tokens only, never literals, apart from logo plate colours, which are the logo's own ground and stay constant across themes (9.4).

### 6.6 Matching the typeface

Never embed the target's own font, even when it can be downloaded. Pick the open-licence match by class:

| The brand's face looks like (by name, or by the site's own fallback stack, or by eye) | Use (Google Fonts, SIL OFL) | Request |
|---|---|---|
| Geometric sans: Avenir, Futura, Circular, Gilroy, Gotham, Cera, Product Sans, Euclid, custom geometrics | **Figtree** | `Figtree:wght@400..800` |
| Neo-grotesque: Helvetica, Neue Haas, Graphik, Aktiv, SF Pro, Suisse, Söhne, Roboto | **Instrument Sans** | `Instrument+Sans:wght@400..700` |
| Humanist sans: Frutiger, Myriad, FF Meta, Gill Sans, Segoe, Calibri | **Source Sans 3** | `Source+Sans+3:wght@400..800` |
| Rounded sans: VAG Rounded, Gotham Rounded, Arial Rounded | **Nunito** | `Nunito:wght@400..800` |
| Serif: Tiempos, Publico, GT Sectra, Canela, Georgia | **Newsreader** (display and body) | `Newsreader:opsz,wght@6..72,400..700` |
| Industrial or condensed: DIN, Eurostile, Tungsten, Knockout | **Barlow** | `Barlow:wght@400;500;600;700` |
| Can't classify | **Instrument Sans** | as above |

If the site's stack names a family that is itself open-licence (for example it self-hosts a Google font), use that exact family, even if it's a common one. Tailoring outranks the "avoid default fonts" instinct here, because the choice is derived, not defaulted.

**Sourcing, with no subsetting tools required.** At build time, request `https://fonts.googleapis.com/css2?family=<request>&display=swap` with a desktop Chrome user agent. Keep only the `/* latin */` `@font-face` blocks, download each `woff2`, and embed it as `url(data:font/woff2;base64,...)` with the same `unicode-range` and `font-display: swap`. Do the same for `IBM+Plex+Mono:wght@400;500`. Budget: 150 KB of font binary in total.

The colophon names the match and says it stands in for the brand's own typeface (section 10).

## 7. Independence cues (all required, every run)

1. The masthead's left slot is the author ("Chris Schubert", with the label "Independent landscape"). The target's name or logo never appears there.
2. The hero eyebrow begins with `INDEPENDENT ANALYSIS`.
3. "Not affiliated with {Target}." is visible at 1440x900 without scrolling (trust panel) and again in the footer.
4. The target's logo tile is the same size as every competitor's. It is never enlarged, never used in a heading, never a background.
5. The brand colour never fills the page ground, the masthead, or any full-bleed band. The largest accent-filled shape allowed is a chip, a bar, a 3px rule or a 2px card border. `--accent-wash` may fill only the target's own column, row or card.
6. Every screenshot sits inside the caption-bar frame (domain, capture date, locale served if not the target market).
7. The target is written about in the third person ("Turo would"), never "we" or "our".
8. Nothing is lifted from the target's site except the labelled screenshot and the unaltered logo: no taglines, product photos, illustrations or icon sets.
9. The colophon states how the accent was derived and that the typeface is an open stand-in.

## 8. Assets: capture, selection, processing, budget

### 8.1 What imagery appears where

| Place | Asset | Size |
|---|---|---|
| Hero cast strip | screenshot (16:10, top of homepage) + identity tile S | about 200px wide per shot |
| Findings exhibits | E1/E2/E3 use tiles; E4 uses an exhibit crop | full exhibit width |
| The field, player cards | screenshot (16:10) + identity tile M | about 400px wide |
| Matrix header, evidence rows, event rail, presence grid | identity tile S | 24px |
| Go-broader cards | identity tile M | 40px |
| Strategy mode, the field's roster entries | identity tile M only; the screenshot (16:10, caption-bar frame) lives in the player drawer, embedded once | 40px tile; about 440px shot in the drawer |

Mobile captures are not used. On a phone, the 16:10 desktop capture still reads as "their homepage", and a second image per company would double the weight for a small-screen nicety. The capture step can stop producing them.

### 8.2 Screenshot capture (per company, including the target)

- Viewport 1440x900 at DPR 1 (or DPR 2 downscaled). Wait for load plus 1.5s of network idle. Scroll to the bottom in 600px steps, return to the top, and wait 1s, so lazy-loaded images fire. Hide consent overlays by injecting `display:none` on fixed or sticky elements whose id, class or aria-label matches `cookie|consent|gdpr|onetrust|cmp|privacy`. Then capture.
- **Gates.** Reject the capture, retry once with doubled waits, then fall back to a manual recapture in an isolated browser (never a signed-in one: a logged-in session can put a name or personalised content on a public page) or to the fallback frame:
  1. **Blocked or challenge page.** The title or visible text matches `just a moment|attention required|access denied|verify you are human|captcha|request blocked|are you a robot|waf`, or the title contains unrendered `{{`. (curl and plain headless Chrome both hit Turo's Cloudflare block page from this machine.)
  2. **Broken imagery.** Any `<img>` in the first viewport with `complete && naturalWidth === 0`, or visible alt text. (Turo's first pass failed this: the hero showed its alt text "Rental reinvented" and three of four car photos were blank.)
  3. **Blank.** More than 92% of pixels within 6 levels of the modal colour.
  4. **Fonts not loaded.** Capture only after `await document.fonts.ready` and `document.fonts.status === 'loaded'`, then 500ms more. (Cityhop's recapture shipped with its headline in Times because the webfont hadn't arrived; a fallback-font screenshot misrepresents the company.)
  5. **Consent modal still covering more than 20% of the viewport.** (Getaround's and Zilch's first passes.)
- `assets.py capture` renders at 1200px wide and steps JPEG quality down 72, 64, 56, 48 to stay under the cap. A manual recapture is normalised with `sips -Z 1200 -s format jpeg -s formatOptions 72 in.png --out assets/<slug>/home.jpg`.
- Record per company: URL after redirects, the locale served (a Sydney machine gets turo.com's Australian site), capture date (Sydney date), status `ok | unavailable`, and a reason.

### 8.3 Exhibit crops (for E4 only)

When a finding's evidence is visible on a page but sits below the fold, capture at 1440x1600 (or full page) and crop to the part that carries the claim. **Aspect ratio between 16:10 and 3:1**, never wider: a 6:1 band scaled into a 7-column exhibit renders its content at about half size, and at phone width it is illegible. If the evidence runs across a wide band (a row of review scores and badges), crop the portion the finding cites and leave the rest out. Test: the key text in the crop must be at least 9px tall when rendered at 358px wide. Store it as `exhibit-<slug>.jpg`, 1200px wide, under the same cap. Record the crop rectangle and the source URL. At most two per page.

### 8.4 Logos: the identity tile system

The captures produce a mix: app-icon squares, transparent wordmarks in any colour, og tiles, and sometimes nothing. **Every company is shown as a square identity tile** of fixed size, radius and border, with its name always set beside it in the page's own type. Uniform squares make the mix look deliberate, and because the name is always adjacent, the tile never has to be legible as a word.

**Selection order** (take the first that passes the checks):
1. A square app icon (`apple-touch-icon`, manifest icon) at least 80px.
2. A square mark from the site (inline SVG or image) inside the header's homepage link, or with `logo` or the company name in its class, id, alt, aria-label or title.
3. A transparent wordmark from the same places.
4. `og:image`, when it's a flat logo tile rather than a photo.
5. A favicon of at least 80px.
6. Otherwise: monogram.

**Mandatory visual check.** Render each chosen asset on white and on near-black and look at it. It must show the company's name or its known mark. Reject:
- Other companies' logos. Review, social, payment and app-store badges turn up constantly: GO Rentals' candidates included the Google and Facebook review logos.
- UI icons and decoration. Turo's first "inline SVG logo" was an AI-sparkle icon (`IconAiSparkleBrand`), and Getaround's was a rating star.
- Photos, mascots and broken files.

**Fill modes** (recorded in the manifest):
- `bleed`: the asset is an opaque square app icon or tile. It fills the tile with `background-size: cover`, centred. Two exceptions, both seen on the Turo run: an icon with transparent rounded corners goes on a plate of its own edge colour (GO Rentals' icon on `#E21266`), and a non-square og tile carrying a wordmark is fitted with `contain` on a plate of its own sampled background colour, never centre-cropped (a crop clipped Getaround's wordmark).
- `plate`: the asset is transparent. It sits centred on a plate colour, with 18% padding each side, at `background-size: contain`. **The plate is the ground the company itself puts behind that logo.** Dark logos go on `#FFFFFF`. Light logos go on the site's header or brand colour, sampled from the screenshot behind the logo, or on `#1A1A1A` if nothing can be sampled. The plate colour is constant across both themes, so the logo is never recoloured or inverted.
- `monogram`: no acceptable asset. The tile is filled `--surface-2` with the initials in `--ink` (the target: `--accent-fill` with `--on-accent`). Initials are the first letter of the first two words, or one letter for a one-word name, in the brand face at weight 700 and 42% of the tile height. The manifest records why.

**Tile spec.**
- Sizes: S = 24px (radius 6), M = 40px (radius 9). There is no larger size. Screenshot fallbacks use M.
- Border: `box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--ink) 14%, transparent)`, so a white plate still has an edge on a light ground.
- Sharpness, measured against the rendered size at M: a `bleed` raster needs a native short side of at least 60px (1.5x of 40). A `plate` raster needs a native width of at least 1.5x its rendered width inside the padded tile (a 154x47 wordmark renders about 26px wide, so it passes easily). An asset that fails at M is not used at S either; take the next candidate, so one company never shows two different marks.
- Rasters are kept as PNG. If over 30 KB, downscale to 160px with `sips -Z 160`. SVGs are sanitised (strip `<script>`, `on*` attributes and external `href`s; keep `viewBox`; remove width and height) and embedded as `data:image/svg+xml;base64`.
- Tiles are `aria-hidden="true"`, because the adjacent name carries the meaning.

### 8.5 Embedding

- Every image is declared **once**, as a CSS custom property in a single `<style id="asset-data">` block placed just before `</body>`:
  `:root{--shot-mevo:url("data:image/jpeg;base64,...");--tile-mevo:url("data:image/png;base64,...");}`
- Components reference them with an inline custom property, for example `<div class="shot" style="--img:var(--shot-mevo)" role="img" aria-label="Mevo homepage, mevo.co.nz, captured 23 September 2026"></div>`, where `.shot{background:var(--img) top center/cover no-repeat}`.
- This keeps the markup readable and makes reuse free: the hero strip and the player card share one copy of each screenshot.
- `check.py` passes `data:` URIs. Still no external `url()`, `src` or `href` fetches of any kind.

### 8.6 Page-weight budget

- `index.html`: hard limit **2.5 MB**, warning at 2.0 MB (add both to `check.py`).
- Per screenshot: `min(180 KB, 1100 KB / number of companies)` of JPEG binary. Per exhibit crop: 180 KB.
- Per tile: 30 KB. Fonts: 150 KB in total. Markup, CSS and JS: 200 KB.
- Base64 adds about 34%. Six companies plus two crops comes to roughly 2.1 MB.

### 8.7 Manifest fields the builder reads

`assets/manifest.json`, keyed by slug: `name`, `domain`, `url_captured`, `locale_served`, `captured`, `shot {file, status, reason, notes}`, `exhibit_crops [{file, source_url, rect, finding}]`, `tile {file, mode, plate, native_short_side, reason}`, `chip {label, variant}`, and for the target `brand {primary, secondaries, near_black, fonts, font_class, font_match}`.

## 9. Components

Each component lists anatomy, then sizes, then states, then responsive behaviour. Sizes are CSS px.

### 9.1 Masthead

- Sticky, `top: env(safe-area-inset-top, 0px)`, height 64 (phone 56), `--bg` fill, 1px `--rule` bottom border, z-index above the matrix's sticky header.
- Left: "Chris Schubert" in the brand face, 15px, 650, `--ink`, followed by the `label` "INDEPENDENT LANDSCAPE" in `--ink-3`, 12px gap. It links to the repo.
- Right: the tablist (9.1a) takes the slot the nav anchors used to hold, right-aligned before the theme toggle. Then the theme toggle: 32px tall, 12px horizontal padding, `label` text naming the theme it switches to ("DARK"/"LIGHT"), 1px `--rule-strong` border, `--r-s`.
- Phone (below 720px): the tablist moves into a second row that is not sticky, two equal-width tabs, 44px tall, centred text, same underline as the masthead version, 1px `--rule` bottom border. It does not scroll sideways; two tabs always fit. The sticky row keeps the author mark and the toggle.

### 9.1a Tabs

- **Two tabs only: Analysis and Evidence and method.** A third nav system layered on top of two tabs would be the overload this split exists to remove, so the five old section anchors (Findings, The field, Compare, Evidence, How it was built) are gone from the masthead; every one of them still works as a deep link into whichever tab holds it.
- **720px and up:** tabs sit in the masthead's right slot, 14px, 500, `--ink-2`, full masthead height, 24px apart. Selected: `--ink` with `box-shadow: inset 0 -2px 0 var(--ink)` on the bottom edge; weight never changes, so nothing shifts on selection. Hover `--ink`. Accent is never used on a tab, because accent means the target. Check the masthead fits at exactly 720px (author block, two tabs and the toggle in one row); if a future run's author block or tab labels are long enough to overflow, raise this floor rather than shortening the independence label.
- **Under 720px:** the tabs fill the second row in place of the old scrolling nav list (9.1).
- **Progressive enhancement.** Ship the tabs as plain links (`<nav class="tabs" aria-label="Page"><a class="tab" href="#top" data-panel="panel-analysis">Analysis</a><a class="tab" href="#evidence" data-panel="panel-method">Evidence and method</a></nav>`), with each tab's sections wrapped in a `<div class="panel">`. Neither panel carries `hidden` in the markup; the router adds it. `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, `role="tabpanel"` and `aria-labelledby` are all added by the script, so a no-JS reader gets ordinary links and both panels simply show, stacked in tab order.
- **One rule for every hash:** the hash names an element, the tab containing it is shown, then the element is scrolled into view. Tab clicks, masthead links, the trust panel, cast cards and back/forward all share this one code path (`hashchange`). Back/forward uses native hash history, and tabs never call `pushState` or `replaceState`, and never use `localStorage`; `pushState` and `replaceState` are allowed only for drawers (9.24). If the target is already in the showing tab, the script does nothing and lets the browser restore scroll natively. Route synchronously at the end of `<body>`, before first paint, so loading a tab-2 link never flashes tab 1.
- **The drawer branch.** The router's first test, before any tab logic, is whether the hash names an article in the drawer registry (9.24). Look it up by registry, never by DOM position: once an article is inside the dialog, `el.closest('[role="tabpanel"]')` returns null and the old code would scroll and focus a hidden element. If it is a drawer id, show the Analysis tab without scrolling, then open the drawer, and stop. Otherwise, if a drawer is open, close it, then run the rule above.
- **Scripts.** Three, in this order: theme toggle, tab router, drawer (the drawer lives inside the router's closure, because both read the hash). No other script is added.
- **Keyboard and ARIA:** roving tabindex, selected tab is 0, the other is −1. Arrow keys, Home and End move focus and activate in the same step, which is safe because both panels are static. Enter follows the link natively; Space is handled by the script. Focus stays on the tab after activation; after a cross-tab jump from any other link, focus moves to the target element with `preventScroll`, and `.panel [tabindex="-1"]:focus{outline:none}` keeps that invisible (the target is a heading or section, not a control). The masthead's `scroll-padding-top:80px` already clears the sticky bar for any of this.
- **Print:** both panels print; tab 2 starts a new page (`break-before:page`); the tabs, the mobile nav row, the toggle and the two end-of-tab links are hidden.
- **End-of-tab links**, most useful on a phone where the tab row scrolls away: a `.tab-next` block closes tab 1, after going broader's ask (9.17); a `data` link "Back to the analysis" closes tab 2, after limits (9.19 area).

### 9.2 Hero

- `padding-block: 72px 48px` desktop, `40px 32px` phone.
- Grid at desktop: headline block in columns 1 to 8, trust panel in columns 10 to 12, aligned to the top of the headline. Tablet: trust panel below, full width, with its `label` spanning the full width on top and the bar plus figures on the left, the fact lines on the right. Phone: stacked.
- **Eyebrow**: `label`, `--ink-3`: `INDEPENDENT ANALYSIS · {TARGET} × {LENS, 2 TO 4 WORDS} · {DD MON YYYY}`. 16px above the headline.
- **Headline**: `display-xl`, `--ink`, at most 3 lines at 1440 (about 85 characters). One phrase, the part about the target's move or advantage, is marked: in `ink` mode it is `--accent` text; in `highlighter` mode it is ink on a brand-fill marker (`background: linear-gradient(transparent 55%, var(--accent-fill) 55%)`, `box-decoration-break: clone`); in `neutral` mode it gets a 3px ink underline. Mark only a phrase about the target. Never mark a competitor's failure in accent.
- **Standfirst**: `lede`, `--ink-2`, 2 or 3 sentences, 24px below.
- **Trust panel**: 1px `--rule` left border, 24px left padding, no fill. It leads with the share of **facts** that carry a re-checked source, as a 44px figure with a one-line caption giving the count (for example "99% · of facts carry a source checked against the page on {date} (106 of 107)"), because judgements can never be Observed and an all-claims ratio undersells the sourcing. Under it, the compact segmented bar of all labelled claims (sourced facts solid; judgements, logged negatives and unconfirmed facts hatched with gaps) and a `data` line with each count. Classify every Inferred line before building (see `reference/revalidation.md`).
  - `label` "HOW FAR TO TRUST THIS".
  - Confidence bar, compact version (9.16): height 10.
  - `data`: "{o}% observed · {i}% inferred" on one line and "{n} claims" on the next, so a wrap never strands a separator at a line end.
  - Three to four `small` lines: "{n} competitors, {k} profiled in full"; "Deep profiles re-checked against the pages they cite on {date}"; "Desk research. No interviews or customer calls."
  - A link, "Evidence and method", to `#evidence`. This is the hero's only link into tab 2, and it names the tab it lands on, so the reader knows where they've gone.
  - Last line, 13px `--ink-3`: "Not affiliated with {Target}."
- **Estimates in the trust panel.** A derived percentage that is estimated rather than counted (a share of facts sorted by wording and corrected with a sample, say) gets the estimate treatment wherever it appears: the "est." prefix, a dotted underline, a superscript `i` (16px at the 44px figure), and a caption that says how it was estimated (the sample size, and what was counted line by line). The hero, the evidence section and the README quote the same figure (rule 9).
- **Cast strip**: 48px below the text block (phone 32). Header row: `label` "THE FIELD" on the left, and `data` "Homepages captured {date}" in `--ink-3` on the right. Then the cast cards (9.3).

### 9.2a Strategy mode

A strategy-mode run is a landscape whose brief is a set of strategy questions (typically three) rather than one framing lens. It changes the fold and the order of the Analysis tab, and nothing else in the frame.

- **The answer row replaces the real market at the fold** (10-second test, item 3). Under the headline, in columns 1 to 8 and in place of the standfirst, a row of one cell per question, equal widths, 24px gap, each with a 1px `--rule-strong` top border and 12px of padding. A cell, top to bottom: a `label` "{n} · {VERB}" ("1 · BECOME", "2 · GET THERE", "3 · WHO BUYS"); one `body-s` sentence in `--ink`, at most 18 words (so the cell runs 4 lines or fewer at 1440), that answers the question rather than restating it; a `data` link in `--ink-3` to `#question-{n}`. Phone: one column, 16px gap. The figure strip (9.6a) must still start above 900px at 1440x900, so the section head above it drops to its `label`.
- **The cast strip leaves the fold.** The market map is an exhibit (E9 is the usual form), so the homepage thumbnails become reference material. When the brief asks for a view of the competitive landscape, the field stays on the Analysis tab as its closing section under a short h2 ("Who is in the market"), after Questions for management (a lead-session ruling, October 2026). Otherwise it moves to the top of the Evidence and method tab, and the Next row says so.
- **Each question is a section** with the anchor `#question-{n}`, opening with its answer (the options or verdict cards) and followed by the findings and exhibits that are the why.
- Questions for management follow the last question, because for a board reader they are the most actionable thing on the page; only the field (when it stays on this tab) comes after them.
- Recommendations that mix "do now" decisions with sequenced build steps follow the split in 9.15.
- **Optional question rail** (9.25) and the compact roster (9.11) belong to this mode.

### 9.3 Cast card (hero)

- The whole card is an `<a href="#player-{slug}">`.
- Anatomy: screenshot (16:10, `--r-m`, 1px `--rule-strong` border, `.shot`). 12px below it, a row with tile S, 8px gap, and the name (15/20, 650, `--ink`). 8px below that, the status chip.
- Grid: up to 6 companies in one row at desktop (`repeat(n, 1fr)`, 16px gap); 7 or 8 companies go 4-up in two rows. Tablet 3-up, phone 2-up. More than 8: show the 8 most relevant, then a `small` line "and {n} more in The field".
- **Target placement encodes the truth.** If the target already operates in the lens market, it goes first. If the lens is a market entry (the target isn't there yet), it goes last, set apart by a 1px `--rule` vertical divider with 24px either side (phone: a full-width divider row). Its chip reads "Not in {market} yet".
- **F1. Seven across.** 7 companies (6 plus the target) go in one row at 1280px and wider, not the 4-up-in-two-rows the 6-company case below implies; 8 or more still go 4-up in two rows. At 7-up each card is about 148px wide, so a chip can hold 15 characters with the alert glyph or 16 without; write ending chips as event plus year ("Collapsed 2026", "Dissolving 2026"). Use the same chip wording for a company everywhere it appears. Confirm on the 1280 capture that no chip wraps. Between 1100 and 1279px, drop to 4-up (the divider hides, same as tablet). Below 1100px, the existing tablet and phone rules apply unchanged.
- States: hover turns the screenshot border `--ink-3` and underlines the name. Focus gets the outline. The target's screenshot border is 2px `--accent-fill`.
- Screenshot unavailable: the fallback frame (9.10) at thumbnail scale, with the tile and domain only.

### 9.4 Identity tile

See 8.4. Class `.tile.tile-s` or `.tile.tile-m`, background from `--tile` and `--plate`. It never stretches, and `flex: none` keeps it square.

### 9.5 Status chip

- Height 22, padding 0 8px, `--r-s`, `label` type at 11px with 0.06em tracking, `white-space: nowrap`, **at most 20 characters** (the cast card is about 176px wide at six across, and a chip that wraps breaks the strip's baseline). For an ending event, the chip names the event and its date ("COLLAPSED MAR 2026", "LIQUIDATING 2026"); what happened next (a relaunch, a sale) goes in the role line and the card summary, never in the chip.
- Variants:
  - `neutral` (owner or model, e.g. "TOYOTA NZ"): 1px `--rule-strong` border, `--ink-2` text, no fill.
  - `alert` (e.g. "ADMINISTRATION · MAR 2026", "LIQUIDATING · 2026"): `--alert-wash` fill, `--alert` text, 1px border in `color-mix(in oklab, var(--alert) 45%, transparent)`, and a 6px square rotated 45 degrees in `currentColor` before the text, with a 6px gap.
  - `subject` ("NOT IN NZ YET", or "SUBJECT"): `--accent-wash` fill, `--accent` text, 1px `--accent-line` border. In `highlighter` mode: `--accent-fill` fill, `--on-accent` text, 1px `--ink` border.
  - `substitute` (the cluster role for a product that replaces the target's without competing like for like, such as a camera maker whose free app counts people): a plain `neutral` chip, no colour and no dashed border (dashed means not done yet, rule 7). Wording is "FREE ON CAMERA" or whatever the substitute is called; the cluster label on its card reads "Substitute".
  - `depth` ("SURVEY DEPTH"): 1px dashed `--rule-strong`, `--ink-3`. ("FULL PROFILE"): 1px solid `--rule-strong`, `--ink-2`.
- One status chip per company per context. Its wording is fixed in the manifest so it reads the same everywhere.

### 9.6 Section head

- `label` eyebrow (what the section is, e.g. "FINDINGS"), 12px gap, then the `h2` headline, which is a sentence that says something, max 30ch. Optionally, 16px below, a one-sentence `body` intro in `--ink-2`, max 60ch.
- It sits in columns 1 to 8. Nothing sits beside it.

### 9.6a Figure strip (F4)

- A row of up to 4 figure cells directly under the Findings section head (9.6), above Finding 1. No cards and no accent: 1px `--rule` dividers between cells, the same construction as the position board (9.13), so it reads as a skim layer rather than four more tiles.
- **F4.** Each cell: the figure (the `figure` type, 4.4), a label (14/20 `--ink-2`, 2 lines max), and a `data` 11px line giving the source domain plus a link to the finding it belongs to (or to another anchor, when the figure supports the positioning section instead of a single finding).
- Figures are Observed, or "est." plus a superscript `i` under the same rule as E6 (9.9). A figure can carry one inferred clause in its label without losing its Observed status, provided the number itself is sourced.
- Desktop 4-up, tablet and phone 2x2. Grid items need `min-width: 0`, or a cell whose label wraps to a long unbreakable word will force its column wider than its share and overflow the row at narrow widths.

### 9.7 Finding block

- `<article id="finding-{n}">`. Desktop grid: text in columns 1 to 5, exhibit in columns 6 to 12, both aligned to the top. Findings are separated by 72px of space, with no rules.
- Text column, top to bottom:
  - `label` "FINDING {n} OF {total}" in `--ink-3`.
  - `h3` headline sentence, 12px below.
  - The lead: `body` in `--ink-2`, at most 30 words (about 3 lines at 1440), 12px below. It is the whole visible argument; nothing in the finding runs longer than 3 lines.
  - "What it means for {Target}": a `label` "FOR {TARGET}" in `--accent`, then one `body` sentence in `--ink`, 16px below.
  - "Why": a disclosure row (9.23) holding the rest of the argument, 16px below. Anything a reader needs to follow the claim stays in the lead; the disclosure holds support. Exhibits never collapse: they carry the visual layer, so the answer to too much text is to cut the prose around them.
  - Sources line: `data` 12px `--ink-3`, e.g. "Observed · 3 sources · Mevo and Getaround profiles", with the profile names as links to `#player-{slug}`.
- **No exhibit available.** The text runs across columns 1 to 7, with the "Why" row under it. The "For {Target}" line moves to columns 9 to 12 as a pull line: 20/30, `--ink`, with a 2px `--accent-fill` left border and 16px padding. Never invent an exhibit to fill the space.
- **F5. Wide-finding variant**, for an exhibit too wide for the 6 columns above (an ownership map (E2) with more than 3 groups, a presence grid (E3) with more than 5 categories): the text runs as a row above, headline and body in columns 1 to 6, the "For {Target}" line and sources in columns 8 to 12 (column 7 left as a gap), and the exhibit spans the full 12 columns below it, 24px below the text row. Use this only when the exhibit genuinely needs the width; a finding whose exhibit fits in 6 columns stays in the standard layout above.
- Tablet and phone: text first, then the exhibit at full width, 24px apart.

### 9.8 Exhibit frame

- `<figure id="exhibit-{n}">`: `--surface` fill, 1px `--rule` border, `--r-l`, padding 24 (phone 16).
- Header: `label` "EXHIBIT {n}" in `--ink-3`, then the title (15/22, 650, `--ink`) on the next line, 20px above the body.
- `<figcaption>`: 20px above, 12px top padding, 1px `--rule` top border, `data` 11.5/18 in `--ink-3`. It holds the source(s), the Observed/Inferred status, and the legend if the exhibit uses a texture.
- **D4. Captions are for readers.** A caption explains the data: what was computed, what's missing and why. It never states an encoding rule ("losses are ink"), a build fact ("gets monogram tiles", "is now sourced to"), or where something sits on the page ("the card sits above"). `check.py` greps for `never alert|monogram tile|now sourced|sits above|per the current profiles` and fails the build if a caption matches.
- Exhibits are numbered in order of appearance on the Analysis tab, and the text refers to them by number.
- At most one exhibit per finding and six in total (the matrix and player cards don't count).
- **Only the eleven exhibit types below exist (E1 to E11).** A builder may not invent a new chart type. If none fits, the finding runs without one.

### 9.9 Exhibit types

**E1 Event rail**: for findings driven by what happened when.
- Only Observed, dated events. Day or month precision is placed; month-only goes at mid-month with a label like "MAR 2026"; year-only events are not placed and belong in the text.
- Horizontal time axis: 1px `--rule-strong`, from the start of the first event's quarter to the end of the last one's. Quarter ticks 6px tall, labelled in `label` `--ink-3` ("Q1 2026"). Positions are on a true time scale.
- Markers, 10px: alert events are a rotated square in `--alert`; other events are a circle in `--ink-2`; target events are a circle in `--accent-fill`.
- Labels alternate above and below the axis, with a 16px connector in `--rule-strong`. Each label is at most 180px wide: date (`data` 11px `--ink-3`), then tile S and company name (13/18, 650), then the event (13/18 `--ink-2`, at most 60 characters). Body height 260.
- **Choose the mode before drawing.** Use horizontal only if every pair of adjacent events is at least 12% of the axis range apart; otherwise use vertical mode from the start. Real event sets cluster (four of Turo's five events fall within ten weeks), so vertical will be the common case, and horizontal is the exception for evenly spread histories.
- Vertical mode (also used under 720px): a vertical line on the left, markers on it, labels to the right, evenly spaced in date order. Where an interval between adjacent events is more than three times the median interval, insert a gap note between them (`label` `--ink-3`, e.g. "13 MONTHS"), so the even spacing doesn't hide the time that passed. The caption adds "Spacing not to scale."

**E2 Ownership map**: for findings about who owns whom.
- A row of groups. Each group has a parent box: `--surface-2` fill, 1px `--rule-strong`, `--r-m`, padding 10px 14px, `label` "OWNER", and the name in 15/20, 650.
- Below it, a bracket: a 12px vertical line from the parent's centre, a horizontal line across the children's centres, and 12px drops to each child, all 1px `--rule-strong` (drawn with CSS borders or pseudo-elements).
- Children: tile M, the name (14/20, 650), and a `data` 11px detail (e.g. "since 2018", "acquired 2026").
- Independent companies sit under a parent box with a dashed border and the label "INDEPENDENT".
- The target, if relevant, sits at the far right, 32px apart, inside a 1px dashed `--accent-line` outline, with its parent (e.g. "IAC · 31% STAKE") and its subject chip.
- Group widths are proportional to child count (`grid-template-columns` in `fr` equal to child count), with a minimum of 152px per group so no parent name wraps.
- **All parent boxes share one height, and all children share one top line.** Build it as one grid with two rows (parents, then children) across every group, or give parent boxes a fixed height of 64px, so a two-word parent name can't push its children below the others.
- An inferred link uses a dotted connector and a superscript `i` on the child.
- Under 720px, groups stack and each bracket becomes a left rule with the children indented 20px.

**E3 Presence grid**: for findings about who does or doesn't have something.
- A table. The first column holds tile S and the name (14/20). Header cells are `label`, at most 6 categories, each at least 88px wide.
- Cell glyphs, 12px:
  - Observed present: a filled `--ink-2` dot, with an optional 12px `--ink-2` name beside it ("AA").
  - Looked, none found: a 1.5px `--ink-3` ring.
  - Inferred present: the same filled `--ink-2` dot as Observed (the thing is claimed to be there), with its name label in dotted underline plus superscript `i` (rule 3: glyphs this small can't carry hatch). Present and absent must never look alike.
  - Not researched: an en dash in `--ink-3`.
- **The column the finding is about comes first**, immediately after the company column, at every width, so it is never scrolled off-screen on a phone. It gets a `--surface-2` band plus 1px `--rule-strong` borders on both sides (the fill alone is only a 3-point lightness step in dark theme and disappears), and a `label` in `--ink` naming the finding ("THE GAP"), set as its own line above the header row, separated from the column's own header by 4px. No accent, because accent is the target's.
- The target's row: `--accent-wash` ground, glyphs in `--accent-fill`.
- The legend is in the figcaption. "None found" is always worded as absence of evidence, never as proof of absence.
- Phone: the table scrolls sideways in its container, with the first column sticky.

**E4 Screenshot exhibit**: for findings where the page itself is the evidence.
- A caption bar (as in 9.10) over an exhibit crop (8.3) or the homepage capture, at full exhibit width, `--r-m`.
- Optional: one verbatim quote from the captured page below it (17/26, `--ink`, in curly quotes), plus a `data` source line.
- No drawn callouts or arrows on the image.
- At most two per page.

**E5 Ordinal band**: for findings about where companies sit on a judgement scale. This generalises v1's moat bar.
- One row per company, 36px tall. The label column is 168px wide (tile S and name). The track spans the rest: `--surface-2`, 12px tall, `--r-s`.
- Range bar: 12px, radius 3, filled `--ink-2` (the target: `--accent-fill`). A wholly or partly inferred range uses `--hatch` with a 1px `--ink-3` outline (the target: `--hatch-accent` with a 1px `--accent-fill` outline).
- Axis: worded ends only ("Minutes", "Weeks") in `label` `--ink-3`, with optional evenly spaced ordinal category ticks (Minutes, Hours, Days, Weeks). Never numbers.
- Bars are clamped inside the track.
- The caption states: "Positions are ordinal judgements. Hatched ranges are inferred."
- Phone: the label sits above the track.

**E6 Figure pair**: for a finding that rests on one or two numbers.
- One or two figures side by side, 40px apart: `figure` type, unit in 16px `--ink-2`, label in 14/20 `--ink-2` (at most 2 lines), source in `data` 11px.
- An inferred figure is prefixed "est.", with a 2px dotted underline and a superscript `i`.
- A pair is allowed only when the two numbers are in the same unit and mean the same kind of thing.
- **Three cells** are allowed when all three show the same kind of change (a from-to on customers, on locations, on staff). Equal columns with 1px `--rule` dividers, the figure at 34px (the cells are narrower than a pair's), and under each a from and to line giving each end's source and its date. No bars: a separate scale per metric makes unlike quantities draw the same length.
- **Dates.** Any dated series carries the date of each claim. A date that records when the page was read, not when the claim was made (an undated About page), is labelled "read {date}", goes in the label line (for example "About page, undated, says 400+"), and is never placed in sequence with claim dates, because sequence reads as a trend that was not measured.

**F2. E7 Signed ratio bars**: for a finding that rests on a ratio several companies report (margin, growth), where the ratio can be negative as well as positive and the honest picture needs them on one shared scale.
- One shared percent axis running through zero, horizontal, with every tick labelled (no unlabelled ticks). The zero position is fixed for the whole exhibit; each row's bar runs from the zero line to the row's value, right for positive, left for negative.
- Rows are grouped (for example "Still operating" then "Stopped"), each group introduced by a `label`.
- **F2.** Each row is a label line (tile S, name, data tag, optional chip), then the track with the value in a 72px right-aligned column (`tabular-nums`), then the inputs line. The layout is the same at every width. Choose the axis domain so the outermost tick labels, centred on their values, stay inside the track at a 258px track width; centre every tick label. Monogram tiles use tile S like every other row. The alert chip marks an ending inside the research year; older or unconfirmed endings use the neutral chip. Inputs lines take one shape: "{amount} {profit|loss} on {revenue} revenue · {source}", or "No accounts published · {source}".
- Only Observed inputs go in; the ratio itself is computed here, and the caption says so.
- The target's bars are `--accent-fill`; every other company's bars are `--ink-2`. Losses are never alert colour, because alert is reserved for ending events, which the chip already carries.
- A bar too thin to read (a result near zero) gets a `min-width` floor so it still shows as a bar with its label, not a sliver that vanishes.
- Rows with no public result stay in the list with an en dash in the value position and "no accounts published" (or equivalent) in the inputs line, so survivorship isn't hidden by omission.
- No other exhibit type may be used to show a ratio that goes negative for some companies and positive for others; that comparison belongs to E7, or to E8 when revenue size is part of the argument.

**E8 Scale against margin**: for a finding about whether a model makes money at scale. x = revenue, log10; y = net result ÷ revenue, linear; one dot per company-year; a company's years joined by an arrow in time order.
- Both coordinates are Observed. The ratio is computed at build time, and the caption says so.
- The log scale is always named in the axis title. Ticks fall on 1-3-10 values, and every tick is labelled.
- y is linear and never broken. Zero is always in the domain and is the strongest line. The domain sits on the 25-point grid and covers every point.
- No trend line, fitted curve, bubble size or third encoding. Three to eight points cannot carry a trend.
- The target is in accent (dots, arrow, name). Others are in ink. Losses are never alert; an ending event is an alert glyph-and-text line under the label.
- Labels go direct on the chart, haloed in `--surface`, and there is no legend. A positive point's label never sits under the zero line.
- Mixed currencies: plot at face value only when no sourced rate exists. Put the currency on every point label and in the caption, and leave the tick labels currency-free. If a plausible conversion could reverse the order the finding rests on (points within a third of a decade), leave that point out and list it in the note.
- Companies with no accounts are named in a one-line note under the chart, so survivorship isn't hidden.
- Build two fixed-geometry SVGs (wide 560×392 at 720px and up, narrow 320×392 below), generated from the data by the scale formulas and swapped with CSS. The narrow version drops the PROFIT/LOSS words.

**E9 Layer stack**: for a finding about which layers of a market exist and where the target sits in them.
- A four-column grid, one row per layer, rows separated by 1px `--rule` with 18px of padding: layer (176px), who is there (flexible), what is happening (236px), the target column (188px), 20px column gap. A header row of `label`s names the columns; the target's is in `--accent`.
- Layer cell: `label` "Layer {n}" in `--ink-3`, the layer name (15/20, 650), a 13/19 one-line description in `--ink-2`.
- Players are tile chips: tile S and name in a 1px `--rule` pill (`--r-m`, 32px tall, 13/18, 600) on `--bg`, with an optional status chip inside it at 18px tall. A player the run named in the market scan but did not profile is plain text in the same pill height (500, `--ink-2`, no tile), so profiled and unprofiled read differently at a glance. The target's pill is on `--accent-wash` with an `--accent-line` border.
- **Pill states when a player opens a drawer.** A profiled player is an `<a href="#player-{slug}">` (9.24) with a 1px `--rule-strong` border (the interactive-boundary use 4.5 reserves); hover turns the border `--ink-3` and underlines the name (`transition: 120ms ease-out`); focus gets the outline. An unprofiled player stays a `<span>` with a 1px `--rule` border and no hover, so the difference reads at a glance. A `data` legend line sits above the exhibit body: "Select a profiled company for its profile." The same states apply to E11.
- A `substitute` (9.5) goes last in its layer, after a 1px `--rule` divider that spans the cell and a `label` "SUBSTITUTE", with its neutral chip inside the pill.
- What is happening: 13/19 `--ink-2`, one or two sentences of Observed trend. Anything that is a judgement says so.
- The target column sits on `--accent-wash` with `--r-m` and 10px 12px of padding. It holds up to two markers, each a 12px dot beside a line: a `label` ("TODAY", "RECOMMENDED") over 13/19 text. A filled dot (`--accent-fill`) means the target operates there today, in the Today line, or the recommendation centres it there, in the Recommended line. A ring (1.5px `--accent-fill`) means an early move today, or a layer the recommendation feeds. Markers are glyph plus text, so colour is never the only carrier.
- The caption gives sources, names the plain-text players as unprofiled, defines filled and ring, and says layer placement is a judgement.
- Under 1100px the grid narrows (150, flexible, 200, 172). Under 720px the header row hides, each layer stacks, and the target cell shows its two markers side by side (one column under 480px).

**E10 Public statements**: for a finding about what the market says in public, and what the target has not said.
- At most four rows, one per vendor: the vendor (tile S and name, 14/20, 650) at 176px, the quote, and the source domain as a `data` link at 150px. 16px vertical padding, 1px `--rule` between rows.
- The quote is verbatim, in curly quotes, 15/23 `--ink`, with an optional 13/19 `--ink-3` context line under it. A source that cannot be quoted verbatim is left out; it is not paraphrased into the column.
- The target's row is last, on `--accent-wash` (`--r-m`, 14px 12px), and holds the negative search: the finding as an inferred line (dotted underline plus superscript `i`, in `--ink`), then a 13/19 `--ink-3` line naming the pages searched and the date. The source slot reads "Absence of evidence, not proof of absence", in the same type as a domain. A negative search is never worded as proof.
- Phone: each row stacks to one column with 8px between the vendor, quote and source.

**E11 Privacy ladder**: for a finding about where players sit on an ordered ladder of practice (how a thing is handled, from most to least protective, say), and where the target sits today and should sit. It reuses E9's grid so the two exhibits rhyme.
- Rungs are rows, the strongest at the top, 1px `--rule` between them. Three columns: rung (176px), who is there (flexible, pills as in E9), the target (220px, on `--accent-wash`, `--r-m`, 12px padding), with a 20px column gap and a header row of `label`s (the target's in `--accent`). A rung cell is a link to its rung drawer (9.24) and holds the `label` "RUNG {n}", the name (15/20, 650) and a one-line meaning (13/19 `--ink-2`). Pills carry a player's placement by its own documents, so the header says so ("Who is there, on their own documents").
- **Target markers are E9's.** A filled dot (`--accent-fill`) in a rung where the target operates today, a ring (1.5px `--accent-fill`) in the rung the recommendation moves it to. Each is a `label` ("TODAY", "RECOMMENDED") over 13/19 text, glyph plus text. Under a marker, an optional `data` 11.5px `--ink-3` line may record how the target describes itself where that differs from the rung.
- **A pending regulatory threshold is a dashed line, not a callout.** Between the two rungs it falls across, a 1px `--ink-2` dashed rule spans the first two columns, with a `data` 11px label above it at the left that says what is pending and when ("EXPOSURE DRAFT, AUG 2026: ..."). Applying the draft to a rung is a judgement, so a word in the label carries the superscript `i`. Dashed means not done yet (rule 7), and a draft is exactly that. The target's marker sits directly under the line.
- **Footer for context figures**: inside the exhibit, above the caption, 24px below the rows, with a 1px `--rule` top border and 20px of padding. One or two E6 figure cells (the pair rule applies: same unit, same kind of thing), then one dated `small` line for the single event that explains why now. The figures are Observed, or "est." with the superscript `i`.
- Under 1100px the columns become 150, flexible, 190. Under 720px the header row hides, each rung stacks (rung cell, pills, then the target cell), a rung whose target cell is empty shows none, and the dashed line spans the full width.
- The caption gives sources, defines filled and ring, and says rung placement is a judgement.

**Price-to-revenue bars** (not a new type: the E7 track and value construction, with one group and one scale): for a finding about what buyers have paid per dollar of revenue.
- One shared linear axis from 0x, ticks labelled on every 2x or so. Rows are grouped, each group introduced by a `label` ("Measurement · sold"). Row: name with a `--ink-2` descriptor, the multiple in a 72px right-aligned `tabular-nums` column, a 14px track, and an inputs line giving price, revenue, period and source.
- Sale bars are `--ink-2`. A **listed peer's market value** may go in as a separate first group, labelled "Listed ANZ peer · market value", with a solid `--ink-3` bar (never dashed, because dashed means not done yet, and never hatched, because the figure is Observed) and a `min-width` floor so a small multiple still shows. Its inputs line gives the date of the quote, since a market value moves daily and a sale price does not.
- A row with no multiple stays in the list with an en dash and the reason, in a "No multiple" group.
- The caption says "read the gaps between groups", never "orders of magnitude": the axis is linear, and a linear axis shows differences, not powers of ten.

### 9.10 Player card and screenshot frame

- `<article id="player-{slug}">`: `--surface`, 1px `--rule` border, `--r-l`, `overflow: hidden`. The target's card: 2px `--accent-fill` border.
- **Caption bar**: height 32, padding 0 12px, `--surface-2`, 1px `--rule` bottom border. `data` 11px `--ink-3`: the domain on the left; the capture date on the right (plus the locale served, e.g. "AU SITE", when it isn't the lens market). The target's bar adds "SUBJECT" in `--accent` before the date. The bar never clips: the date keeps `flex: none`; the left item takes `min-width: 0; overflow: hidden; text-overflow: ellipsis`; and below 480px any descriptor between domain and date ("BELOW THE FOLD", "AU SITE") is dropped.
- Screenshot: 16:10 `.shot`, top-anchored. **A screenshot always renders at its captured 16:10 aspect.** `.shot` never gets `aspect-ratio: auto`, `min-height` or a flex-stretched height, because `cover` into a box of any other shape crops the company's logo and headline off the sides.
- **Fallback frame** (screenshot unavailable): the same 16:10 box in `--surface-2`, centred column: tile M, the domain (`data`), and a `small` `--ink-3` line at most 30ch wide, e.g. "Homepage not captured on 23 Sep 2026: the site blocked automated access." It never looks broken, and it never pretends.
- Body, padding 20 (phone 16), top to bottom:
  - A header row: tile M, 12px gap, the name (`h4`), then the status chip on the right (wrapping below on narrow cards).
  - The role line, 8px below: `label` `--ink-3`, e.g. "NZ CAR-SHARE · FREE-FLOATING · WELLINGTON".
  - The summary, 12px below: `body-s` `--ink-2`, 2 to 4 sentences.
  - The depth row, 16px below: the depth chip, then a mini confidence bar (120 by 6, 9.16), then `data` "{o} observed · {i} inferred".
  - A disclosure, 16px below, with a 1px `--rule` top border and 12px padding: `<details>`, whose `<summary>` is "Key facts and sources" (14px, 600) with a CSS chevron. Inside is a list of 4 to 8 facts in `body-s`. Observed facts end with their source domain as a `data` link. Inferred facts get the dotted underline and a superscript `i`. The last line reads "Full profile: profiles/{slug}.md" and links to the GitHub blob.
- **Wide variant, retired as the default (F3).** When the hero cast strip already shows every competitor's homepage at a glance (9.3), a second, larger capture per card is the same picture twice, so the player card no longer carries its own screenshot at the top. Instead: tile M, name and chip | role line | 2 to 4 sentence summary | depth chip, mini bar and counts | one `<details>` labelled "Homepage, key facts and sources", holding, in order, the caption-bar-framed 16:10 screenshot, 4 to 6 facts with source domains, then the profile link. Every card uses this one shape regardless of cluster size, so there is no wide card and no shot-col; a cluster's odd-one-out no longer needs special-casing. Keep the old two-column wide variant (screenshot column at 58%, body at right, screenshot always visible) only for a run with no hero cast strip to lean on. In strategy mode the card is not on the page at all: it is the body of the player drawer (9.24), and its disclosure opens by default there.

### 9.11 The field: roster grid

- **Strategy mode: compact roster.** With no cast strip above it, the field is a thumbnail grid nobody on a board needs at a glance, so it becomes a roster with no screenshots (those live in the player drawer, 9.24). Entries are grouped under `label` rows (the cluster names, 32px between groups, 12px under each label), Subject last. Each entry is an `<a href="#player-{slug}">` card: `--surface`, 1px `--rule-strong`, `--r-l`, padding 16, a 40px tile M, the name (15/20, 650) and the status chips in a wrapping row, then a 13/19 `--ink-2` role line across the full width, at most two lines, which is set by the copy and never clipped. The target's card is 2px `--accent-fill` (padding 15). Hover turns the border `--ink-3` and underlines the name. Grid: 4-up from 1100px, 2-up from 720 to 1099px, 1-up below, `align-items:start`. A chip is one status per company, worded as everywhere else.

- **D6.** When most clusters would hold one card, drop the cluster rows: the field is one grid in cast-strip order (9.3), 3-up at desktop, 2-up from 720 to 1099px, 1-up below. Each card's first line, above its header, is its cluster as a `label` (e.g. "Corporate car share", "Peer-to-peer, NZ", "Stopped", "Traditional rental", "Subject" in `--accent` for the target). The section h2 carries the clustering thesis, since no cluster sentence is left to repeat it.
- `align-items:start` on the grid, so opening one card's disclosure doesn't stretch its neighbours.
- Every company appears once, under its current cluster label. Past membership (e.g. "Mevo, before its relaunch") is mentioned in its card body, not shown as a second card.
- The target's card is last, carrying the "Subject" label, matching its divided slot in the hero cast strip.
- A `substitute` (9.5) carries the cluster label "Substitute" and the neutral chip, with no colour and no dashed border.
- **If a run's clusters are genuinely uneven** (most hold two or more cards, so the grid would bury the grouping), fall back to the older cluster-row layout: cluster text in columns 1 to 4, cards in columns 5 to 12 (2-up, 20px gap), 1px `--rule` top border and 72px between clusters, with a "FOR {TARGET}" line only where the cluster carries a point no finding already makes.

### 9.12 Comparison matrix

- Wrapped in an `overflow-x: auto` container with the legend above it: `data` 11px, e.g. "Dotted underline and i mean inferred. A dash means not researched at this depth."
- **D7.** At 1100px and wider, the matrix fits its container: `table-layout:fixed`, a 120px dimension column (via `<colgroup>`), and the companies sharing the rest equally, with 10px cell padding and 13/19 body text from 1100 to 1279px. Below 1100px it scrolls in its container at a fixed minimum width (1000px for 7 companies; scale with the count). Never let the target's column be the one cut off at desktop width.
- Table: the first column has a `--bg` fill, sticky left only while its own container is scrolled sideways. The header row is **not** sticky: `position: sticky` inside an `overflow-x` container sticks to the container, not the page, so it can't work here.
- Header cells: tile S and the name (13/18, 650), aligned to the bottom, padding 12. The target's header has a 3px `--accent-fill` top border, with the `label` "SUBJECT" in `--accent` above the name.
- Row headers: `label` `--ink-3`, wrapping.
- Body cells: 14/21 `--ink`, padding 12px 10px, 1px `--rule` bottom border.
- The target's column: `--accent-wash` ground from top to bottom.
- Inferred cell: the cell text gets a dotted underline (1px, `--ink-3`, 3px offset) plus a superscript `i` in `--ink-3`, per rule 3. No hatch strip: a 4px strip sits on the column boundary and reads as belonging to the neighbouring cell.
- Not researched: an en dash in `--ink-3`, with `title="Not researched at this depth"`.
- Under 720px it transposes to one `<details>` per dimension. The summary is the dimension name; the content lists each company (tile S, name, value), with the target's row on `--accent-wash`. Generate both markups and switch between them with CSS.

### 9.13 Position board (strengths, gaps, open ground)

- Three columns at desktop, separated by 1px `--rule` vertical lines with 32px padding; stacked on phone.
- Column headers: `label` "STRENGTHS", "GAPS", "OPEN GROUND", each preceded by its glyph (+, −, ○) in the brand face at 20px, `--ink`.
- Items are 20px apart: a 24px glyph gutter (the same glyph in 16px `--ink-3`), a title that is a short sentence (16/24, 650), and detail (15/23 `--ink-2`, 1 to 2 sentences).
- No colour, no cards. Item shapes vary as the voice doc requires.

### 9.14 Option comparison (lens deep-dive, optional)

- Two or three option cards side by side: `--surface`, 1px `--rule`, `--r-l`, padding 24.
- Each card: the option name (`h4`), then rows of a `label` plus `body-s` for "WHAT IT BUYS", "WHAT IT COSTS" and "WHO IT REACHES", then a one-sentence verdict at the bottom above a 1px `--rule`.
- The option the analysis recommends: 2px `--accent-fill` border plus a subject-variant chip, e.g. "SHARPER FIRST MOVE". Costs stay qualitative unless a source gives a figure.
- Phone: stacked.

### 9.15 Recommendations

- An `<ol>`. Each item is a two-column grid: a 64px numeral (brand face, 40/44, 700, `tabular-nums`, `--ink-3`; the first item's numeral is `--accent`), then the content.
- Content: the headline (`h3`), the body (`body`, `--ink-2`, at most 70 words), and a `data` 11px "Rests on" line with links to `#finding-{n}` and `#exhibit-{n}`.
- Items are separated by 1px `--rule` lines and 28px vertical padding.
- Order is the analysis's priority. The count is whatever the analysis gives.
- **Decisions now versus build steps.** When the recommendations mix decisions the reader can take today with steps that must happen in sequence, split them into two lists under two heads. First, "Decisions now" (for a board, "Two decisions for the board now"): an unnumbered list, same item construction without the numeral column, because nothing in it is ordered. Second, the build steps, "Four build steps, in order": the numbered `<ol>` above, each item carrying a time chip ("0 to 6 months"). Numbering must never contradict a time chip: a NOW item numbered last under a head that says "ordered by what unlocks most" breaks rule 8. The decisions list comes first, because it is what the reader can act on.

### 9.16 Confidence bars (Evidence section)

- **Main bar**: 16px tall, radius 3, as a flex row. Each segment has `flex: {count} 1 0` (flex-basis 0, so the ratio is exact). Observed is solid `--ink-2`. Inferred is `--hatch` on `--surface-2` with a 1px `--rule-strong` outline. Below each segment, a `data` 12px label: "{o}% OBSERVED · {n} CLAIMS" and "{i}% INFERRED · {m} CLAIMS".
- **F6. Segmented inferred bar**: when the Inferred share breaks down into more than one kind of claim (judgements by design, logged negatives, facts that couldn't be confirmed), split the Inferred segment itself into one sub-segment per kind, each still `--hatch`, separated by a 2px `--bg` gap so the eye reads three bars rather than one. This is additive to the two-segment bar above, not a replacement; use it only when the breakdown is worth showing on its own.
- **F6. Before-and-after pair**: two compact (10px) bars stacked, one per re-check date, each labelled with its date and ratio ("{date} · {pct}% of {n} claims"), and a one-line caption naming what changed the base (a competitor added, claims split or merged), so a reader doesn't read the shift as the research getting less rigorous.
- **Per-profile rows**: tile S and name (168px), the depth chip (112px), a bar (8px tall, same construction), and `data` "{o} / {i}". Full profiles are listed first, then survey depth, alphabetical within each group.
- **F6. Evidence table** (replaces the per-profile rows above when a re-check note exists to join them to): one row per profile, combining the label bar (O/I, as above) with a second bar for the re-check result (solid `--ink-2` confirmed, solid `--ink-3` corrected or stale, `--hatch` could not confirm) and its "{n} checked" count, plus a count of judgements the re-check found resting on a wrong premise. A profile re-checked on a different schedule than the rest (for example, sourced with verbatim quotes on first pass rather than re-checked later) gets a row with its label bar and a one-line note in place of the re-check bar, not a fabricated re-check count.
- **D8.** A header row names the three measures (labels, re-check, wrong premise); no per-row label repeats a column heading (the measure name goes in the header, not beside every value). The target row's wash stays inside the table edges, never a negative margin that bleeds past the container. On phone, each row stacks label bar then re-check bar, with the wrong-premise count written out beside the company name rather than hidden.
- **D8.** The main bar's labels (9.16 above) sit under their own segments, not as one line to the side; the inferred breakdown stacks under the inferred part specifically, so the reading order matches the bar's left-to-right order.
- **Verification line**: a `--surface-2` box, `--r-m`, padding 20, `body-s`. **F7.** The fixed wording parameterises its scope: "Every sourced claim in {scope} was re-checked against the page it cites on {date}. Claims whose sources couldn't be reached or didn't support them were corrected or downgraded to inferred." `{scope}` is "the deep profiles" when only the full-depth set was re-checked, or names the actual set when it differs (for example "all six profiles" or "five profiles ... Camplify sourced ... the same day"); the rule-10 wording itself ("re-checked against the pages they cite", never "verified true") never changes.
- **Estimated figures.** When the leading figure is estimated rather than counted, it gets the estimate treatment (9.2) in the evidence section too, and the note under the bar says how it was estimated. The evidence tab leads with that same figure and the segmented bar, not a second pair of unrelated counts (rule 9).
- **Compact variant** (hero trust panel and player cards): the same construction at 10px or 6px, without the labels under the segments.
- The section headline states the ratio as a sentence.

### 9.17 Open questions and going broader

- Open questions: an unnumbered list in `body`, at most 6.
- **Going broader**: an `h3` sentence, then one card per survey-depth competitor: a 1px **dashed** `--rule-strong` border (dashed means not done yet), `--r-l`, padding 20. Each card: tile M, the name, and a depth chip; then "A full profile would answer:" with a `body-s` list.
- Close with a `body` line: "A full profile with the same citation check takes a few hours. Ask: {contact}". The contact is shown as selectable text and also linked.
- **Going broader ends tab 1**, followed by the Next row (9.1a) into tab 2.

### 9.18 Part 2 opener band

- Full bleed, `--surface-2` fill, `padding-block: 96px` (phone 64), 1px `--rule` top and bottom.
- Contents: the `label` "HOW THIS WAS BUILT" (no "Part 2", since the tab now does the parting), a `display-l` headline (a sentence about the process as an asset), and a `lede` standfirst. The standfirst and everything after it in tab 2 never says "above" or "below" to mean a position on the page; tab 2 doesn't share a scroll position with tab 1, so say "on the Analysis tab" instead.
- This is the one register change on the page.

### 9.19 Process rail

- A horizontal stepped rail (a real sequence, so numbered): one column per skill that ran, with a 1px `--rule-strong` connector running through the step numbers.
- Each step:
  - The number (`data` `--ink-3`).
  - The command in a code chip (`data` 13px, `--surface` fill, 1px `--rule`, `--r-s`, padding 4px 8px), only when the step is a real command the reader could run. A step that happens inside another command (the citation check runs within `/competitive-update`) gets a plain `label` instead, e.g. "INSIDE /COMPETITIVE-UPDATE".
  - What it does (15/22, 650).
  - What it produced in this repo, with real counts ("5 profiles written, 3 taken deep"), in 14/20 `--ink-2`.
- **D10.** The command or label slot above each step title has a fixed minimum height (two chip rows, 66px), so titles line up across the rail even when one step carries a plain label, one a code chip, and another two stacked chips. Under 720px the slot's minimum height drops to 0, since the rail is vertical there and nothing needs to line up.
- Under 720px it turns vertical, with the connector on the left.

### 9.20 Why this compounds

- An `h2` sentence, then a 2x2 grid (phone: 1 column) of four blocks with a 32px gap. Each block: a `label`, an `h4` sentence, and `body-s` text.
- The blocks cover:
  - Living profiles and diffs.
  - Additive depth.
  - Regeneration from source.
  - Commits as a market timeline.
- The first block carries a small inline specimen: the three diff sorts ("MATERIAL", "MINOR", "NO CHANGE") as neutral chips.
- Use this repo's real state (counts, dates, commands), never generic language.

### 9.21 Label specimen and plain documentation sections

- **Labelling discipline**: two rows. On the left, the profile line exactly as it appears in the markdown (`data` 13px, `--surface-2`, `--r-m`, padding 16): one Observed line with its URL and one Inferred line. On the right, how that claim renders on this page: the solid versus hatched bar segment, the matrix edge, the dotted underline and `i`. This ties the method to the visuals.
- **Material change, trust boundary and limits** use plain documentation layout: columns 1 to 8, `h2` labels allowed as plain labels (per the voice doc), `body` text.

### 9.22 Footer and colophon

- 1px `--rule` top border, `padding-block: 48px`. Desktop: two columns; phone: stacked.
- Left, `body-s` `--ink-2`: "Independent analysis by Chris Schubert. Not affiliated with {Target} or any company named here. Logos and screenshots identify each company and belong to their owners; screenshots were captured from public homepages on {date}."
- Right, `data` 11px `--ink-3`: "Accent derived from {Target}'s public brand colour {hex}. Type: {Font} (SIL Open Font License), an open stand-in for {Target}'s own typeface, which is not used here. Data and labels in IBM Plex Mono. Built {date} from {repo link}."

### 9.23 Disclosure row

Prose that supports a claim goes in a disclosure, never in a second column and never in a tooltip. Native `<details>` and `<summary>`, stacked, never side by side (an open panel squeezed into a third of the width is unreadable).

- **Labels are fixed:** "Why" (the rest of the argument), "Evidence" (source and date detail), "What it takes" (the capability, partner or cost behind a step). Do not invent others. A row takes the word, 8px gap, then an optional hint.
- **Summary:** `min-height: 44px`, flex, `cursor: pointer`, with a 1px `--rule` top border on the `<details>`. The word is 14/20, 600, `--ink`. The hint is `data` 11.5/16 `--ink-3`, at most 40 characters, naming what is inside so the click has a scent ("two local rivals, the deals"). A recommendation row omits the hint where the label alone says enough.
- **Chevron:** CSS only, a 7px square with 1.5px `--ink-3` right and bottom borders, at the far right, rotated -45deg closed and 45deg open, `transition: transform 120ms ease-out`. Hide the default marker (`list-style: none` and `::-webkit-details-marker`). Focus per 4.6.
- **Body:** padding `4px 0 20px`, gap 12, `body-s` in `--ink-2`, max 66ch. An inline variant, inside an exhibit or a card, drops the top border and the max width and may use 13/19 or smaller type.
- **Ranked-list variant** (a ranked list of options, buyers say, where each row's summary carries the answer): an `<ol>` of rows. The summary is a grid of a 48px numeral (40/44, brand face, `--ink-3`, every rank, since none of these is the target), the type (18/24, 650), the candidates (14/22 `--ink-2`) and the why (14/22 `--ink`, at most 14 words), then the chevron; the body is indented 64px, max 80ch, with `label`-style run-in heads for its parts. Under 1100px: numeral, type and chevron on one line, candidates and why below in column 2. Under 720px: a 32px numeral at 24/32, candidates and why full width.
- **Print and no JS:** the rows work natively without a script. `beforeprint` opens every `<details>` that is closed (recording which, and `afterprint` restores them), and `.dx::details-content{content-visibility:visible}` is a Chromium-only bonus that must not be relied on. Chevrons are hidden in print.
- **Find-in-page:** Chrome expands a closed `<details>` to show a match; other engines may not. Accept it.

### 9.24 Side drawer

Disclosures hold prose; drawers hold entities (a company, a rung of a ladder). Nothing a reader needs to follow the argument is only in a drawer.

- **Markup.** One `<dialog class="drawer" id="drawer">` at the end of `<body>`: an inner wrapper (`padding: 0 24px 32px`, phone 16px), a sticky bar holding only a "Close" button, and an empty body. The contents are ordinary `<article id="player-{slug}">` and `<article id="rung-{n}">` nodes in a `#profiles` appendix at the end of tab 1 (a `.prof-grid`, under an h2 "Profiles and privacy rungs" for the no-JS reader). The article's own header is the drawer's heading: a `label` kind line ("PROFILE · LAYER 1 · CAPTURE"), tile M, the name as an `h4` with an `id` and `tabindex="-1"`, and the status chip. Do not duplicate the name in the shell.
- **Move, never clone.** On open the router moves the article from the appendix into the dialog body; on close it moves it back to its recorded parent and next sibling. Cloning would duplicate ids, so `getElementById`, the hash and `aria-labelledby` would all hit the hidden original. At load, build an id lookup of every appendix article; the router's drawer branch (9.1a) reads that lookup. If `showModal` is missing, skip the drawer entirely and leave the appendix visible.
- **Hide the appendix with CSS, not `hidden`:** `@media screen { .js-drawer #profiles { display: none } }`, with `js-drawer` added to `<html>` by the script only once the lookup is built. Print then needs no override beyond `@media print { .js-drawer #profiles { display: block } }`.
- **Geometry.** `showModal()` plus the UA dialog style reset, or the drawer will not be full height or right-aligned: `margin: 0; inset: 0 0 0 auto; max-width: none; max-height: none; height: 100dvh; padding: 0; border: 0; border-left: 1px solid var(--rule-strong); border-radius: 0; overflow: auto; overscroll-behavior: contain` (so iOS does not scroll-chain to the page). Width `min(480px, calc(100vw - 48px))`; below 720px `width: 100%` and no left border (not `100vw`, which overflows when a classic scrollbar is present). Background `--surface`, no shadow. `::backdrop { background: var(--scrim) }`. Lock the page behind it with `html:has(dialog[open]) { overflow: hidden }` plus `html { scrollbar-gutter: stable }` so nothing shifts.
- **Sticky bar.** `position: sticky; top: 0`, `--surface`, 1px `--rule` bottom border, 12px padding, the Close button right-aligned: `label` type, 32px tall, 12px padding, 1px `--rule-strong`, `--r-s`.
- **Motion.** The drawer-in of 4.6: `translateX(16px)` and opacity from 0 on desktop, `translateY(16px)` on phone. The offset lives in the fixed top layer, so it cannot widen the document.
- **One closeDrawer(), synchronous.** It calls `dialog.close()`, moves the article back, and clears `aria-labelledby`. Escape (route the `cancel` event through it with `preventDefault()`), a click on the backdrop (`e.target === dialog`), the Close button and `beforeprint` all call it. Do not hold state in the `close` event, which is dispatched asynchronously in every engine.
- **Opening.** Set `aria-labelledby` to the article's heading id, `showModal()`, then in a `requestAnimationFrame` focus that heading with `preventScroll`. Reset the dialog's `scrollTop` to 0 at the same point, and again after `load` and `document.fonts.ready` unless the reader has already scrolled (wheel, touch, key), because late layout can leave a tall article scrolled partway. `showModal()` makes the page inert and traps focus natively; never hand-roll a trap.
- **Focus return.** Chrome blurs a link on fragment navigation, so by the time `showModal()` runs `document.activeElement` is `<body>` and native restore goes there. Record the opener in a document `click` listener, and on close refocus it in a `requestAnimationFrame` with `preventScroll`, falling back to `#top` (given `tabindex="-1"`) when there is no opener (a deep link) or it is gone.
- **History.** Links are plain `href="#player-{slug}"`. A document click listener handles any link whose hash is in the lookup: `preventDefault()`, then
  - from the page: `pushState({drawer:1}, '', href)` and call `route()` directly (`pushState` fires no `hashchange`), recording the opener;
  - from inside an open drawer (drawer to drawer): `replaceState(history.state, '', href)` and call `route()`, so a chain of drawers never stacks entries and Close always takes one press.
  The `{drawer:1}` tag marks an entry an in-page open pushed. **Close** calls `history.back()` only when `history.state.drawer` is set; otherwise (a deep link, a reload, or arrival by Back or Forward) it calls `replaceState(null, '', path + search + '#top')` and stays on the page. Never synthesise a back entry with `pushState` on load: Chrome marks entries added without user activation as skippable. Back while the drawer is open closes it natively through `hashchange`.
- **Pills and links.** Anything that opens a drawer is an `<a>` with a hash; the pill states are in 9.9 (E9). A rung cell and a player name inside a drawer are links too.
- **Player drawer body** (the player card of 9.10, in this order): role line, a 2 to 3 sentence summary, the rung line ("Rung 3 · pseudonymous at the edge", linking to its rung drawer; the target's drawer shows each rung it sits on), the 16:10 screenshot in its caption-bar frame, "Key facts and sources" (4 to 8, rendered open), then the profile path. **Rung drawer body:** the rung's definition, then one row per player: a verbatim quote from its own documents, a source domain, and, where its marketing sits higher than its documents, a line saying so.
- **Print.** `beforeprint` calls `closeDrawer()` synchronously (`history.back()` is async and loses the race with print layout), opens every `<details>`, and `afterprint` restores both. The `.drawer`, Close buttons, scrim and chevrons are hidden in print and the appendix prints.
- **Acceptance tests.** Every build with a drawer must pass these four, smallest first. Playwright's `emulateMedia('print')` applies CSS but does not fire `beforeprint`, so dispatch the event by hand.
  1. **Deep link, then tab 2, Back, Close.** Load `index.html#player-{slug}`, follow an in-drawer link to a tab 2 anchor, press Back (the drawer reopens), press Close: the page stays on the page and focus lands on `#top`.
  2. **Drawer to drawer, then Close takes one press.** Open a player, follow its rung link, press Close: the drawer is gone and the URL is the page's, with no earlier drawer reopened.
  3. **Focus returns to the opener.** Click a pill, press Close: `document.activeElement` is that pill.
  4. **Print.** Open a drawer, dispatch `new Event('beforeprint')`: the dialog is closed, the appendix holds every article, and every `<details>` is open. Dispatch `afterprint`: the earlier state returns.
  Also check at 390 that `scrollWidth === 390` with a drawer open, with Close visible without scrolling, and with scripts disabled that the appendix is visible and every drawer link scrolls to it.

### 9.25 Question rail (optional, strategy mode, desktop only)

- A short list of links in the masthead between the author block and the tabs: "1 Become · 2 Get there · 3 Who buys", one entry per question and never more than three, each linking to `#question-{n}`. `data` 12.5/20 `--ink-3`, 20px apart, `white-space: nowrap`; hover `--ink`. The current question is `--ink` with `aria-current="true"` and a 2px inset underline like the tabs. Accent is never used.
- It exists only at 1100px and wider, only on the Analysis tab, and only once the answer row (9.2a) has left the viewport, so the fold never shows two copies of the same answer. An `IntersectionObserver` on the answer row toggles it; the current question is the last section whose top is at or above 140px, updated in a throttled `scroll` handler. With no JS it is absent. It is hidden in print. It is a masthead addition, so check the masthead still fits at exactly 1100px.

## 10. Deliberately not charted, and banned

- Not charted: geography (no maps), incommensurable scale markers, recommendation timelines (no dates exist), radar charts, sparklines, donuts or any angle-encoded proportion, and scatter plots of inferred positions on numeric axes (an Observed scatter is allowed only as E8). Mixed currencies plotted on one axis are allowed only under E8's rule (9.9): face value, no sourced conversion, and never where a plausible rate could reverse the finding.
- Banned styling: gradients on grounds, glassmorphism or backdrop blur, drop shadows, emoji, decorative icons, centred hero layouts, accent bars on rounded cards, and full-bleed brand colour.
- Banned content moves: invented exhibits, callouts drawn onto screenshots, recoloured or inverted logos, and taglines or imagery lifted from the target.

## 11. Build and verify

Drawers: run the four acceptance tests in 9.24.

Tabs: after one arrow-key press the focus ring is still on a tab, and a phone tab tap shows the whole tab row with its underline.

1. `python3 check.py`: the self-contained and em-dash gates, plus the size gate (warn at 2.0 MB, fail above 2.5 MB).
2. Capture and look at: 1440x900 light, 1440x900 dark (the 10-second test, both themes); a full page at 1440 light; a full page at 1280, 1100 and 1024 (**D9**: the F1 7-up minimum and the 4-up band and matrix-fit floor, both of which only show their bugs at these sizes); and a full page at 390 in light and dark. Use `?theme=` to force the theme. **Since the two-tab split:** `#evidence` at 1440 and 390; `#method` at 390 (it must land on the band, under the sticky bar, with no flash of tab 1); one keyboard pass (Tab into the tablist, then arrows, then Enter); back and forward across a tab change; a JS-disabled capture; and print emulation (tab 2 starts a new page).
3. On the captures, check that nothing overlaps (event-rail labels, ownership brackets, chips wrapping), that every tile is square and sharp, that no screenshot shows a blocked page or broken image, and that the target column's wash reads in dark.
4. Confirm the Observed/Inferred numbers in the hero, the evidence section and the README are the same count.
5. Read the Part 1 copy straight through against `dashboard-voice.md`.

## 12. Per-run block (top of the generated CSS)

```
/* LANDSCAPE PER-RUN BLOCK
   target:        {name} ({domain})
   lens:          {lens}
   brand primary: {hex}  (source: theme-color | css-frequency | logo; confirmed against screenshot)
   secondaries:   {hexes} (recorded, not used)
   near-black:    {hex or none} (source)
   accent mode:   light {ink|highlighter|neutral} / dark {...}; alert clash: {yes|no}
   font class:    {class} -> {OFL family} (brand face: {name}, not embedded)
   target slot:   {first | last, divided}  (operates in lens market: yes|no)
   tiles:         {slug: mode/plate} ...
   exhibits:      F1 {type}, F2 {type}, ...
   captured:      {date}, locale served per company if not the lens market
*/
```

Tokens are pasted below this block from `derive_tokens.py --css`, and rebuilds reuse them unchanged unless the brand colour changes.
