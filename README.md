# ProcurePro competitive analysis

A worked example of an AI-run competitive research process, applied to [ProcurePro](https://procurepro.co), the Australian construction procurement platform. Five competitors, framed on **AI data moats** and **automated workflows**, read across the markets ProcurePro is expanding into.

**Start here: [`dashboard.html`](dashboard.html)** (download and open it, or view it through [htmlpreview](https://htmlpreview.github.io/?https://github.com/cschubertwork/ProcurePro-Competitive-Analysis/blob/main/dashboard.html)). Two tabs: the analysis, and an explainer of how the process works.

Everything in this repository was produced by running the three skills in [`.claude/skills/`](.claude/skills). You can run the same process on your own company.

## What it found

Everyone in the category claims a data moat, and no two are made of the same material.

| Company | Moat is made of | Automation depth |
|---|---|---|
| **ProcurePro** | Awarded trade packages, priced scope, exclusions | Extract, structure, compare |
| Autodesk (BuildingConnected, TradeTapp) | The bid graph: invites, bids, wins, sub financials | Recommend, extract |
| Procore | Project system of record | Agents that act |
| Felix (ASX:FLX) | Vendor compliance and performance | Announced, largely unshipped |
| Causeway | UK invoice and transaction flow | Finance workflow automation |
| Kojo | Live materials spend | Agents that transact |

Two conclusions worth the read: ProcurePro's corpus is the narrowest on the list and the only one sitting inside the moment project value is committed, and the category moved from reading documents to executing workflow steps in about twelve months, which is a gap rather than a defeat.

## The competitors, and why these five

Chosen for a top-five brief requiring at least one Australian competitor and several global players matched to ProcurePro's expansion markets (UK, Middle East, North America).

- **Autodesk** and **Procore** are the incumbents in North America, the market ProcurePro is entering with its Series B.
- **Causeway** is the UK incumbent, in ProcurePro's most developed expansion market.
- **Felix** is the Australian rival, headquartered in Brisbane like ProcurePro.
- **Kojo** sits adjacent to the category. It buys materials for subcontractors where ProcurePro buys subcontractors for head contractors. It is included because it is the clearest working example of a procurement data moat built from transaction flow.

[`reference/competitors.md`](reference/competitors.md) also lists who was deliberately left out and why.

## How to read the sourcing

Every claim in every profile carries one of two labels:

- `- Observed: [claim] ([URL])` is a fact with a source attached
- `- Inferred (assumption): [claim]` is a judgement that nobody published

Roughly 60% of this analysis is Observed and 40% Inferred. That ratio is stated on the dashboard and the inferred cells in the comparison matrix are individually marked. Where a vendor's own marketing claim could not be corroborated, it is recorded as a claim to verify.

## Layout

```
reference/          product positioning, competitor list, profile template
profiles/           one profile per competitor, 10 sections each
analysis/           the cross-competitor analysis
dashboard.html      the two-tab visual dashboard
.claude/skills/     the three skills that produced all of the above
templates/          scaffolding used by /setup for a new company
```

## Running it on your own company

With [Claude Code](https://claude.com/claude-code) in this directory:

```
/setup                          # your product, your competitors, your comparison template
/competitive-update --all       # research every competitor, classify what changed
/generate-analysis <topic>      # cross-competitor analysis on any dimension you name
```

`/setup` asks what dimensions decide deals in your market and builds the profile template from your answers, so the section structure is not fixed to the one used here. Re-running `/competitive-update` appends to existing profiles, and nothing is written to a profile without line-by-line approval.

## Caveats

This is desk research from public sources, produced on 8 August 2026. There are no win/loss interviews, customer calls or analyst briefings behind it. Published announcements are a lagging and partial view of what any company has running with customers, so nothing here should be read as an audit of a competitor's internal capability. Pricing is inference throughout, because none of the six companies publishes it.

Not affiliated with ProcurePro or any company named here. All trademarks belong to their owners.
