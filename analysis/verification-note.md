# Verification note

*Re-check of 10 October 2026, run to `reference/revalidation.md`. Covers every line in the six profiles, `reference/product-info.md`, `reference/competitors.md` and the analysis.*

The first version of this analysis was produced on 8 August 2026, before the engine had a citation check. Its sources were linked but never re-fetched, and 48 of its 82 labelled claims (59%) were Observed. This note records what a full re-check found.

## How it was run

One researcher per company (ProcurePro and the five original competitors), one for the completeness of the competitor set, and one for market context. Each re-fetched every cited page on 10 October 2026 with `curl` or headless Chrome (never a summarising fetch tool), recorded a verbatim quote for every sourced fact, and sorted every line into fact, judgement or negative:

- **Facts** needed a quote from a page fetched that day, or a dated archive capture where the live page blocks automated access (some Autodesk, Business Wire and Buildertrend pages). Syndicated and aggregator sources were replaced with primary ones: ASX announcements for Felix, SEC filings for Procore and Autodesk, Companies House filings for Causeway and ProcurePro's UK company, the ABN register for ProcurePro's Australian entity.
- **Judgements** stay Inferred. Each factual premise under them was checked, and judgements resting on a wrong premise were rewritten or removed.
- **Negatives** ("no list price found") carry the searches that were run.

The lead session re-fetched the claims the analysis now turns on: Procore's agent list on its support site, the Autodesk University 2026 post (Wayback capture of 22 September 2026), E1's Quote Analysis help article, and Felix's ASX header and annual report.

## Counts

| File | Facts with a re-checked source | Facts that could not be confirmed | Judgements and logged negatives |
|---|---|---|---|
| profiles/autodesk-buildingconnected.md | 27 | 3 | 21 |
| profiles/causeway-technologies.md | 27 | 1 | 26 |
| profiles/estimateone.md | 63 | 3 | 42 |
| profiles/felix-group.md | 38 | 0 | 25 |
| profiles/kojo.md | 25 | 2 | 25 |
| profiles/procore.md | 35 | 1 | 22 |
| reference/product-info.md | 58 | 3 | 5 |
| reference/competitors.md | 32 | 0 | 11 |
| reference/market-context.md | 15 | 1 | 7 |
| **Total** | **320** | **14** | **184** |

**95% of facts (320 of 334) carry a source re-checked on 10 October 2026.** This is a count, not an estimate: the lead session read every Inferred line and classified it by hand as a judgement, a logged negative or an unconfirmed fact. The split between judgements and negatives is approximate; the fact count is exact. Each of the 14 unconfirmed facts stays labelled Inferred with "could not confirm on 2026-10-10".

On the measure the first version reported (the share of all labelled lines that are Observed), the figure moved from 59% (48 of 82) to 62% (320 of 518). The base grew because compound bullets were split so each line carries one claim, and E1 was added. Judgements stay Inferred by design, which is why the share of facts is the better measure of sourcing.

Ten Observed lines picked at random were checked against their held quotes; all ten matched.

## Changes that altered a finding

1. **The award decision is not unattended.** The first version said "nobody credible is serving the head contractor's award decision with agentic depth" and that Procore's agents pointed at RFIs, submittals and contract review. Procore's Pro AI package includes a Bid Leveling Agent and a Bid Analyzer Agent, and Procore made the package generally available on 23 July 2026, before the first version was written. The finding is withdrawn and replaced: bid levelling became a feature in 2026.
2. **A missing competitor.** E1 (EstimateOne), which calls itself Australia's leading construction tender platform, was not in the set. It compares two to five quotes per trade package with AI, documented in the UK from October 2025 and in Australia from April 2026, and it merged with the UK's C-Link in July 2025. It is now profiled, and it replaces Felix as the home-market rival the analysis watches.
3. **Autodesk's network outside the US.** The first version called BuildingConnected's network "close to worthless" outside North America and a "cold start" in Australia and the UK. BuildingConnected launched in the UK, Ireland, Australia and New Zealand in October 2020, and no network-size data for those markets was found. The claim is withdrawn.
4. **Autodesk has an agent.** The matrix said Autodesk had no agentic framing. At Autodesk University in September 2026 it announced a Bid Proposal Agent (beta, US) that extracts cost breakdowns, inclusions and exclusions from subcontractor proposals, under the line "AI that acts".
5. **Causeway's shape.** Causeway was described as PE-owned. Five Arrows holds a significant minority stake, and Causeway's directors state there is no single controlling party. It already sells tender management with bid comparison, and it registered an Australian company in 2025.
6. **Felix's position.** "Announced, largely unshipped" is stale: Bid Insights is in customer validation. Most of Felix's reported 51% ARR growth came from acquiring Nexvia. Felix raised A$5.54m in September 2026, and its FY26 accounts show a A$4.0m working-capital deficiency. The "combined Nexvia go-to-market for FY27" is not in any filing and is removed.
7. **Kojo's agents.** "Agents that transact" rested on Kojo's own wording, which says its agents "assist". Execution is not shown independently, so the claim is softened.

## Other corrections

- ProcurePro: founded 2020, not 2019. Its assistant is AI Pulse, not "AI CoPilot". The 104 headcount had no source and is removed. Hansen Yuncken does not appear anywhere on ProcurePro's site and is dropped as a named customer. Payapps, Power BI and Trimble are not on its integrations list. "90% of spend committed early" appears on its homepage; its Series B release says 80%. Both are its own figures.
- Autodesk: Payapps ownership moved from inferred to sourced (10-Q, 20 February 2024, US$387m). The "350,000 projects" figure dated from 2021 and was replaced with current vendor figures.
- Procore: "16,000+ companies" was not on the cited page and is replaced with SEC figures. R&D spend was the FY2023 number and is updated. The Datagrid acquisition closed on 16 January 2026 for US$168.0m. ProcurePro's Procore Marketplace app shows 209 installs.
- Causeway: turnover, ARR and headcount now come from Companies House accounts. The "beyond human logic" campaign quote could not be found and is deleted. "59,000 suppliers" is now "60,000+".
- Felix: all four syndicated (kalkine) citations were replaced with ASX documents. "115,000 vendors" could not be confirmed and is replaced with the ASX figure. A new CEO (April 2026) and CFO (August 2026) were added.
- Kojo: the CEO changed from Maria Davidson to Micah Rodman by April 2026. Funding is now sourced to TechCrunch, Business Wire and Digital Commerce 360 in place of an aggregator.
- Competitor list: Oracle's relevant product is Aconex, which has a tender module (not an ERP). Archdesk's exclusion as "residential, SMB" is stale, since it now sells subcontractor tendering with side-by-side compare.

## Not settled

- What E1 keeps from analysed quotes. Its terms allow training on anonymised data; its Quote Analysis FAQ says inputs are "not retained or used for training".
- Whether Procure Pro Holdings Pty Ltd is ProcurePro's group parent (ASIC extract not obtained).
- Whether Causeway's summer 2026 LetsBuild release to UK clients shipped.
- Whether Kojo's Micah Rodman is a co-founder.
- Measured accuracy for any company's bid comparison. None is published.
