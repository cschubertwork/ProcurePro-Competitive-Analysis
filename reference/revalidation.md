# Re-check pass

The citation check in phase 4 re-fetches the Observed claims in the deep profiles. The re-check goes further, and it is the step to run before a landscape repo is published or shown to anyone. It came out of the Turo run (3 Oct 2026), where the first citation check passed but a full re-check overturned the analysis's lead finding (Getaround had been read as fleet-financed; its 10-K describes a no-fleet marketplace), corrected two owners, found a missing competitor, and showed that two of the citation check's own "corrections" were wrong.

## What it covers

Every claim in every profile, the target's product-info, the analysis (exec summary, matrix cells, cluster and positioning lines) and `reference/competitors.md`. That includes **Inferred lines and table cells**, which the citation check never looks at; most of the errors live there.

Sort each claim into one of three kinds, and treat them differently:

- **Fact** (checkable, whatever its current label): needs a verbatim quote from a page fetched today, or a dated archive capture when the live page blocks automated access. Re-fetch Observed claims too; pages change.
- **Judgement** (comparison, implication, risk, opportunity): never "confirmed". Check each factual premise it rests on and fix or delete the line if a premise is wrong (for example a shareholding that never existed, or a partnership that ended).
- **Negative** ("no sponsorship found", "never operated here"): run and log real searches. One counter-example fails it.

Verdicts: confirmed, corrected, stale, contradicted, could not confirm; for judgements, premises OK or premise wrong.

## Sources

- Primary first: the company's own site and help centre, regulatory filings (SEC EDGAR, the NZ Companies Office register or the local equivalent, stock-exchange announcements), government pages, press releases. Then reputable news. Aggregators (Sacra, Tracxn, PitchBook, TipRanks, StockTitan, comparison blogs) are weak; replace them wherever a primary source exists.
- **Ownership claims go to the company register.** A trade-press "becoming a subsidiary" that the register doesn't show is written as reported, not done.
- WebFetch summarises through a model, so it is not safe for verbatim quotes. Fetch with `curl` (a browser user agent), and with headless Chrome `--dump-dom` for JS-rendered pages and help centres. Python's urllib lacks CA certificates on python.org builds.
- Wayback captures are acceptable when the live page blocks bots; cite the archive URL and its capture date.

## Also check the set itself

One pass asks whether the competitor set is complete: list every business in the market the target would meet (including adjacent vehicle classes or categories that run the target's model), live or dead, with evidence of status. A missing live player that runs the target's model invalidates claims like "no one competes head-on".

## Running it

Fan out one researcher per company plus one for set completeness and one for market context (regulation, insurance, market size), each writing a claim-by-claim file with quotes. The lead session then:

1. **Adjudicates conflicts itself** against primary sources: researchers disagree (one called a dead platform live from an archive capture; one read a former shareholder as current), and the lead's rulings go in one file that every later step follows.
2. Has each profile rewritten from the verdicts and rulings (one writer per file), keeping judgements labelled Inferred and adding at most a handful of material new facts.
3. Audits that every URL on an Observed line appears in the evidence files, or fetches it.
4. Classifies every remaining Inferred line as judgement, negative or unconfirmed fact. Report both numbers: the share of all claims that are Observed, and the share of **facts** that carry a re-checked source. The second is the honest measure of sourcing; judgements can never be Observed.
5. Updates `analysis/verification-note.md` with a dated re-check section: per-ledger counts, the changes that altered a finding, and any earlier correction that turned out wrong, said plainly.
6. Regenerates the analysis if any finding changed, then rebuilds the dashboard.

Context facts the analysis relies on that belong to no profile (licensing, tourism figures, market size) go in `reference/<market>-context.md` with Observed and Inferred labels, outside the profile count.
