# Autodesk (BuildingConnected + TradeTapp)

*Category: Direct | Researched: 2026-08-08*

## 1. Snapshot

- Observed: BuildingConnected and TradeTapp are Autodesk's preconstruction products, covering bid management, bid boards and subcontractor prequalification (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk Construction Cloud has been folded into the Autodesk Forma industry cloud and now carries the Forma brand (https://adsknews.autodesk.com/en/news/autodesk-construction-cloud-is-now-autodesk-forma/)
- Observed: over 350,000 projects use Autodesk Construction Cloud for preconstruction workflows (https://investors.autodesk.com/news-releases/news-release-details/over-350000-projects-turn-autodesk-construction-cloud)
- Inferred (assumption): Autodesk also owns Payapps, an existing ProcurePro integration partner, which puts it on both sides of the procurement-to-payment boundary.

## 2. AI data moat

**The strongest supply-side network in the category, and the hardest for anyone to replicate.**

- Observed: BuildingConnected operates the largest crowdsourced network in commercial construction, used to vet subcontractors and compare financial health (https://construction.autodesk.com/products/buildingconnected/)
- Observed: the Recommendation Engine suggests bidders based on location, trade expertise and past performance (https://resources.imaginit.com/building-solutions-blog/what-s-new-in-autodesk-construction-cloud-2026-a-practical-guide-to-the-latest-features)
- Observed: TradeTapp Financial Data Extraction uses AI to turn PDF financial statements into structured data, giving a fuller view of subcontractor financial health (https://resources.imaginit.com/building-solutions-blog/what-s-new-in-autodesk-construction-cloud-2026-a-practical-guide-to-the-latest-features)
- Inferred (assumption): the corpus is bid-graph shaped. Autodesk knows who was invited, who bid, who won and how the winner was financially rated, across a very large share of US commercial work. That compounds every time a GC runs a tender.
- Inferred (assumption): what Autodesk does **not** have at ProcurePro's granularity is the priced, line-item scope of the awarded package with exclusions attached. Their data is about *who*, ProcurePro's is about *what and for how much*.

## 3. Automated workflows

- Observed: Autodesk AI spans BuildingConnected Pro, Bid Board Pro and TradeTapp, aimed at reducing busywork in preconstruction (https://resources.imaginit.com/building-solutions-blog/what-s-new-in-autodesk-construction-cloud-2026-a-practical-guide-to-the-latest-features)
- Observed: subcontractor qualification is automated via custom questionnaires, limit calculations and financial ratios (https://construction.autodesk.com/products/buildingconnected/)
- Observed: a Bidding tool Beta in Autodesk Forma brings BuildingConnected's bid management and prequalification workflows into the Forma preconstruction experience (https://www.autodesk.com/blogs/construction/autodesk-forma-march-2026-construction-releases-built-for-whats-next/)
- Inferred (assumption): the automation is recommendation and extraction, not agentic execution. Autodesk is behind Procore on the "agents that act" framing, and has said less about it.

## 4. Product overlap with ProcurePro

Covers well: Tenders, Vendor Management, prequalification.
Covers partially: Compare & Recommend, at bid level rather than priced scope level.
Does not cover: Procurement Schedule, Scope of Works Library, Contracts & eSignature as a commercial workflow, Lessons Learnt.

- Inferred (assumption): the overlap is real on the front half of the funnel (find and qualify bidders) and thin on the back half (compare priced scope, award, contract). ProcurePro's depth sits exactly where Autodesk's stops.

## 5. Market position and geography

- **North America:** dominant. This is the incumbent ProcurePro's US entry has to work around.
- **UK:** present through Autodesk Construction Cloud, weaker on bid management specifically.
- **ANZ:** present via Autodesk generally; BuildingConnected's network effect does not transfer, because the subcontractor network is US-dense.
- Inferred (assumption): the network moat is geographically bounded. In Australia and the UK, BuildingConnected is close to a cold start, which is why ProcurePro has been able to win at home.

## 6. Pricing & packaging

- Observed: pricing is not published. Quotes run roughly US$3,600 to US$5,000+ per year, varying by size, users and geography, and some subcontractors report cost tied to their annual revenue (https://downtobid.com/blog/how-much-does-bid-board-pro-cost)
- Observed: a free entry-level tier exists for subcontractors, with paid Pro features (https://downtobid.com/blog/how-much-does-bid-board-pro-cost)
- Inferred (assumption): free-for-subs is the network play. Autodesk subsidises the supply side to keep the graph dense, then charges the GCs who need to search it.

## 7. Differentiators vs ProcurePro

- The network. In the US a GC can find and qualify subcontractors they have never worked with, which ProcurePro cannot offer on day one.
- Financial risk data on subcontractors, via TradeTapp, is a capability ProcurePro does not have.
- Single-vendor consolidation for firms already standardised on Autodesk.

## 8. Risks for ProcurePro

1. **US entry meets a dense network ProcurePro cannot match.** Highest likelihood. Buying decisions in US preconstruction default to BuildingConnected.
2. **Forma Bidding Beta deepens down-funnel.** If Autodesk adds priced-scope comparison to the Forma bidding tool, it lands directly on ProcurePro's core.
3. **Payapps ownership.** Autodesk can bundle procurement to payment and squeeze the integration story ProcurePro currently benefits from.

## 9. Opportunities for ProcurePro

- Autodesk's data answers "who should bid". ProcurePro's answers "is this price and scope right". Positioning against the network rather than trying to build one is the cheaper fight.
- Autodesk is slow on agentic workflow. BidLevel already does something Autodesk has not shipped.
- Outside North America the network advantage largely evaporates, which favours ProcurePro in the UK and Middle East.

## 10. Open questions

- Does the Forma Bidding Beta roadmap include priced line-item comparison and scope-gap detection? This is the single most important thing to watch.
- Is Autodesk training models on the bid graph, or only using it for retrieval and recommendation?
- What is Autodesk's plan for Payapps relative to procurement workflows?
