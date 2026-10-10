---
name: build-dashboard
description: Render the landscape dashboard (index.html) from the current profiles and analysis - a single self-contained page themed to the target company's brand, with each competitor's real homepage and logo, one exhibit per finding, and the method section. Use for /build-dashboard, "rebuild the dashboard", "update the dashboard", or after any profile or analysis change.
---

# build-dashboard

Regenerate `index.html` at the repo root from the current state of the repo. The dashboard is always rebuilt whole from its sources; never hand-edit it and never patch the previous version.

## Sources

- **`reference/dashboard-design.md` is the law** for visuals: layout, components, encoding rules, independence cues, the brand-to-token procedure, the asset spec. Read all of it before building.
- **`reference/dashboard-voice.md` is the law** for the copy. Read it before drafting and write to it the first time.
- **`templates/dashboard.html` is the reference implementation**: a working page built to the design doc (the Turo run). Start from its CSS and markup patterns rather than writing components from scratch, then replace every piece of content, the per-run block and the tokens. Components the analysis doesn't need are deleted, never left empty.
- Content comes from the analysis in `analysis/` (excluding `analysis/updates/` and `analysis/verification-note.md`), the profiles in `profiles/`, and `reference/product-info.md`. `analysis/verification-note.md` feeds the verification line. The README supplies framing (why these competitors, caveats) so the page and the README never disagree.

## Step 1: capture brand and assets

Skip to step 2 if `assets/manifest.json` exists and every company in it was captured within the last 30 days; otherwise capture everything again so the capture dates are consistent.

```
python3 assets.py capture <target-slug> <target-url> <slug> <url> ...
```

One slug per company, the target included (use the homepage URLs in `reference/competitors.md`). This runs headless Chrome in a throwaway profile: it dismisses consent banners, loads lazy images, rejects bot walls and broken captures, and writes `assets/<slug>/home.jpg`, logo candidates, brand signals and `assets/logos.png`.

Then **look at every image** (Read each `home.jpg` and `logos.png`). The script can't judge:
- **Screenshots:** a leftover modal, a half-loaded hero, a regional site (record the locale served; it goes in the caption bar), or anything personalised. A site the script marks BLOCKED gets the design doc's fallback frame. If you capture one by hand, use an isolated browser, never a signed-in one, and normalise it with `sips -Z 1200 -s format jpeg -s formatOptions 72 in.png --out assets/<slug>/home.jpg`.
- **Logos:** pick one tile per company by the selection order and mandatory visual check in the design doc (section 8.4). Candidates regularly include other companies' badges, UI icons, mascots and broken SVGs. Record each choice and why in the per-run block.
- **Exhibit crops** (design doc 8.3), when a finding's evidence is on a page below the fold: `python3 assets.py exhibit <name> <url> <top> <height> [<left> <width>]` (aspect between 16:10 and 3:1, cropped to just the part the finding cites), then look at it and adjust the crop.

## Step 2: derive the brand layer

1. Pick the brand colour by the order in design doc 6.2, confirming it against the target's screenshot. Take the near-black from the manifest's `near_blacks` if it's the target's own.
2. `python3 derive_tokens.py '<brand hex>' [--dark '<near-black>'] --css` and paste the three token blocks as printed. Never hand-pick a hex.
3. Match the typeface by the table in design doc 6.6, then `python3 assets.py font "<Family spec>" "IBM+Plex+Mono:wght@400;500"` and paste the printed `@font-face` rules.
4. Write the per-run block (design doc section 12) at the top of the CSS. On a rebuild, reuse the existing block and tokens unless the brand colour changed.

## Step 3: count, then build

- **Count the labels first** (encoding rule 9): `- Observed:` and `- Inferred` lines per file in `profiles/*.md`. Every ratio on the page, and in the README and the analysis's Data Confidence section, quotes this one count. If the prose elsewhere disagrees, fix the prose.
- Build in the design doc's page order (section 3), pairing each finding with at most one exhibit from the six allowed types. A finding with no fitting exhibit runs without one.
- Reference images and fonts by their `assets/...` paths (screenshots and tiles as CSS custom properties in the `asset-data` block). The embed step inlines them.

## Step 4: embed and gate

```
python3 assets.py embed
python3 check.py
```

`check.py` must pass: it fails a page that still references `assets/`, fetches anything external, or exceeds 2.5 MB, and it catches em dashes. Keep the unembedded page out of the repo; rebuild from sources rather than editing the embedded file.

## Step 5: look at it

Capture and read, using Chrome over the DevTools protocol with mobile emulation (the Chrome CLI's `--window-size` has a minimum width, so its phone-width shots are fake):
- 1440x900 in light and dark: the 10-second test in design doc section 1. All four answers must be visible without scrolling.
- Full page at 1440, at 768, and at 390 in light and dark.
- `document.documentElement.scrollWidth` equals the viewport width at 390, 768, 1024, 1100, 1280 and 1440. No horizontal page scroll. Check the matrix and any wide exhibit at 1100 and 1280 too; those are where seven-company layouts break.

Check that nothing overlaps or truncates (chips, event-rail labels, ownership brackets), every tile is square and sharp, no screenshot shows a blocked page or broken image, and the target's wash reads in dark. Then read the whole page's copy straight through against `reference/dashboard-voice.md`: count contrastive-parallelism instances, check every headline is a sentence that says something, cut intensifier tics.

## Depth honesty

- Survey-depth profiles carry the dashed "Survey depth" chip wherever they appear, and a go-broader card at the end.
- If `analysis/verification-note.md` exists, state that every sourced claim in the deep profiles was re-checked against the page it cites on its date, with the counts. Never phrase this as claims being verified true.
- A claim with no source anywhere in the repo (including snapshot-table cells) is shown as inferred.

## Design review

Every dashboard gets a review by samantha (product design lead) before it ships, covering both `dashboard-design.md` and `dashboard-voice.md`. Apply her must-fix findings and rebuild. The review becomes optional after two consecutive runs with no structural findings. So far that bar hasn't been met: Turo and the ProcurePro rebuild (both 23 Sep 2026) each surfaced findings that changed the design doc (wide-card cropping, E3 glyph honesty, crop aspect, levelled cells), and the Turo re-validation rebuild (3 Oct 2026) added E7 signed ratio bars, the figure strip, compact player cards and the build-note caption gate. Ask her for a page plan before building when the analysis has changed shape, and for the review after; ask her to write both to a file; her hand-back text doesn't always reach the lead session. A structural fix that should apply to every run goes into the design doc and `templates/dashboard.html` in the engine, not only into this repo.
