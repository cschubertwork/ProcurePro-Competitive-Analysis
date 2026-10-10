# ProcurePro competitive analysis

A worked example of an AI-run competitive research process, applied to [ProcurePro](https://procurepro.co), the Australian construction procurement platform. Six competitors, framed on **AI data moats** and **automated workflows**, read across the markets ProcurePro is expanding into.

**Start here: [the dashboard](https://cschubertwork.github.io/ProcurePro-Competitive-Analysis/).** One page: the analysis first, with each competitor's homepage and the exhibits behind every finding, then how the process works. It is a single self-contained HTML file ([`index.html`](index.html)) with the images and fonts embedded and no external requests, so it also works offline if you clone the repo.

Everything in this repository was produced by running the skills in [`.claude/skills/`](.claude/skills). You can run the same process on your own company.

## What it found

Bid levelling became a feature in 2026. ProcurePro's BidLevel is shipped and free to try, and by October Procore, E1 and Autodesk each had their own AI that reads and compares subcontractor quotes. What a newcomer can't copy is ProcurePro's history of awarded packages, so the analysis turns on whether every comparison draws on it.

| Company | Moat is made of | AI bid comparison, October 2026 |
|---|---|---|
| **ProcurePro** | Processed trade packages: quotes, priced scope, exclusions | BidLevel, shipped, free to try |
| Autodesk (BuildingConnected, TradeTapp) | The bid graph: invites, bids, sub qualification | Bid Proposal Agent, beta, US |
| Procore | Project system of record | Bid Leveling Agent, generally available |
| E1 (EstimateOne) | Tender invitations and quotes across ANZ | Quote Analysis, shipped (UK October 2025, Australia April 2026) |
| Felix (ASX:FLX) | Vendor compliance and performance | Bid Insights, in customer validation |
| Causeway | UK invoice and transaction flow | Tender comparison, AI not shown |
| Kojo | Materials orders | Not its buyer |

The first version of this analysis (8 August 2026) said nobody served the award decision with AI. A full re-check on 10 October 2026 found that wrong: Procore's levelling agent was already on sale. [`analysis/verification-note.md`](analysis/verification-note.md) lists every change.

## The competitors, and why these six

Chosen for a top-five brief requiring at least one Australian competitor and several global players matched to ProcurePro's expansion markets (UK, Middle East, North America). The re-check added a sixth.

- **Autodesk** and **Procore** are the incumbents in North America, the market ProcurePro is entering with its Series B.
- **Causeway** is the UK incumbent, in ProcurePro's most developed expansion market.
- **E1** calls itself Australia's leading construction tender platform. It was added in the re-check because it compares quotes inside the same trade packages ProcurePro does, and since merging with C-Link it sells into the UK as well.
- **Felix** is the listed Australian rival, headquartered in Brisbane like ProcurePro.
- **Kojo** sits adjacent to the category. It buys materials for subcontractors where ProcurePro buys subcontractors for head contractors, and it is the clearest working example of a procurement data moat built from transaction flow.

[`reference/competitors.md`](reference/competitors.md) lists who was left out and why, and [`reference/set-completeness.md`](reference/set-completeness.md) lists every business a head contractor could buy for this job, live or dead.

## How to read the sourcing

Every claim in every profile carries one of two labels:

- `- Observed: [claim] ([URL])` is a fact with a source attached
- `- Inferred (assumption): [claim]` is a judgement nobody published, or a fact that couldn't be confirmed

On 10 October 2026 every line was re-checked against the page it cites, fetched that day, with a verbatim quote held for each sourced fact. 95% of facts (320 of 334) now carry a re-checked source; the other 14 are labelled as unconfirmed. Comparisons, rankings and recommendations are judgements and stay labelled as such. A claim re-checked against its page is not thereby true: a vendor's figure supported by its own site is still the vendor's claim.

## Layout

```
reference/          product positioning, competitor list, profile template
profiles/           one profile per competitor, 10 sections each
analysis/           the cross-competitor analysis
index.html          the dashboard, one self-contained page
check.py            the publish gate every commit passes
.claude/skills/     the skills that produced all of the above
templates/          scaffolding used by /setup for a new company
```

## Running it on your own company

With [Claude Code](https://claude.com/claude-code) in this directory:

```
/setup                          # your product, your competitors, your comparison template
/competitive-update --all       # research every competitor, classify what changed
/generate-analysis <topic>      # cross-competitor analysis on any dimension you name
/build-dashboard                # render index.html from the profiles and analysis
python3 check.py                # the publish gate
```

`/setup` asks what dimensions decide deals in your market and builds the profile template from your answers, so the section structure is not fixed to the one used here. Re-running `/competitive-update` appends to existing profiles, and nothing is written to a profile without line-by-line approval.

## Caveats

This is desk research from public sources, first produced on 8 August 2026 and re-checked in full on 10 October 2026. There are no win/loss interviews, customer calls or analyst briefings behind it. Published announcements are a lagging and partial view of what any company has running with customers, so nothing here should be read as an audit of a competitor's internal capability. Pricing is mostly inference, because only E1 publishes a list price for builders.

Not affiliated with ProcurePro or any company named here. All trademarks belong to their owners.
