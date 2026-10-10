# Autodesk (BuildingConnected + TradeTapp)

*Category: Direct | Researched: 2026-10-10 (re-checked)*

## 1. Snapshot

- Observed: Autodesk lists a BuildingConnected product family of BuildingConnected Pro (bid management for general contractors and owners), Bid Board Pro (bid management for subcontractors) and TradeTapp (subcontractor qualification) (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk states that Autodesk Construction Cloud is now Autodesk Forma, announced 24 March 2026 (https://adsknews.autodesk.com/en/news/autodesk-construction-cloud-is-now-autodesk-forma/)
- Observed: the BuildingConnected product page states a network of 1.5M+ construction professionals and says builders use it on 2M+ projects (vendor claims, as of 2026-10-10) (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk's 10-Q says it acquired 100% of Payapps Limited on 20 February 2024 for total consideration of $387 million in cash (https://www.sec.gov/Archives/edgar/data/769397/000076939724000091/adsk-20240430.htm)
- Observed: the Payapps website now describes the company as "Payapps - An Autodesk Company" (https://www.payapps.com/)
- Inferred (assumption): owning Payapps puts Autodesk on both sides of the procurement-to-payment boundary in ANZ and the UK. Payapps does not appear on ProcurePro's public integrations list (checked 2026-10-10), so the earlier description of it as a ProcurePro integration partner is dropped.

## 2. AI data moat

**Inferred (assumption): the strongest supply-side network in the category, and the hardest for anyone to replicate.**

- Observed: Autodesk says BuildingConnected gives access to "the largest crowdsourced network to vet subcontractors, compare financial health, and expand your trusted partnerships" (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk says BuildingConnected's Recommendation Engine suggests bidders based on location, trade expertise and past performance (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk says TradeTapp's Financial Data Extraction uses AI to turn PDF financial statements into structured data (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk says "Some Autodesk AI-powered features do not leverage machine learning and so do not require data for training of the underlying models." (https://construction.autodesk.com/products/buildingconnected/)
- Observed: in October 2020 Autodesk said there were "more than one million construction professionals on the BuildingConnected network in North America alone", with over 2,000 general contractors and owners bidding out projects totalling $56 billion in project value (https://www.nasdaq.com/press-release/autodesk-expands-buildingconnected-into-emea-and-apac-to-give-global-construction) (dated, six years old)
- Inferred (assumption): the corpus is bid-graph shaped. Autodesk knows who was invited, who bid, who won and how the winner was financially rated. That compounds every time a GC runs a tender. The premises (invitations, bids, financial data held in the products) rest on the Observed lines above.
- Inferred (assumption): what Autodesk does **not** have at ProcurePro's granularity is the priced, line-item scope of the awarded package with exclusions attached. Their data is about *who*, ProcurePro's is about *what and for how much*. Caution: Autodesk's Bid Proposal Agent (Beta, section 3) now extracts cost breakdowns, inclusions and exclusions from proposal PDFs into Forma Bid, so the gap is narrowing at the single-bid level (searched Autodesk construction blog and BuildingConnected pages for any dataset of awarded line-item scope, none found, 2026-10-10).

## 3. Automated workflows

- Observed: Autodesk says "Autodesk AI enhances preconstruction workflows in BuildingConnected Pro, Bid Board Pro, and TradeTapp", listing the Recommendation Engine, Bid Forwarding and TradeTapp Financial Data Extraction as features "currently available" (https://construction.autodesk.com/products/buildingconnected/)
- Observed: subcontractor qualification is automated via custom questionnaires, limit calculations and financial ratios, per Autodesk (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Autodesk's March 2026 Forma release notes list a Bidding tool [Beta] that brings BuildingConnected bid management and prequalification workflows into Autodesk Forma (https://web.archive.org/web/2026/https://www.autodesk.com/blogs/construction/autodesk-forma-march-2026-construction-releases-built-for-whats-next/)
- Observed: at Autodesk University 2026 (blog updated 11 September 2026) Autodesk said it is "expanding beta access to Forma Bid for BuildingConnected customers (on Autodesk licensing)", and that teams will "soon" be able to link Forma Estimate line items to bid packages to compare subcontractor pricing against estimates and identify scope gaps; the scope-gap capability is announced as upcoming, not shipped (https://web.archive.org/web/2026/https://www.autodesk.com/blogs/construction/autodesk-university-2026-forma-product-highlights-across-the-construction-lifecycle/)
- Observed: Autodesk lists a Bid Proposal Agent (Beta) that "analyzes proposal PDFs and extracts key details, including cost breakdowns, inclusions, and exclusions, into structured bid data within Forma Bid" (https://web.archive.org/web/2026/https://www.autodesk.com/blogs/construction/autodesk-university-2026-forma-product-highlights-across-the-construction-lifecycle/)
- Observed: Autodesk describes its AU 2026 direction as "moving from AI that assists to AI that acts", with three new agentic capabilities highlighted in the keynote (https://web.archive.org/web/2026/https://www.autodesk.com/blogs/construction/autodesk-university-2026-forma-product-highlights-across-the-construction-lifecycle/)
- Observed: the Forma Bid beta is available for the Forma hub in the US region and requires a Takeoff subscription with the Preconstruction product enabled (Autodesk developer blog, April 2026) (https://aps.autodesk.com/blog/buildingconnected-api-enhancements-connected-workflows-forma)
- Inferred (assumption): the GA features are recommendation and extraction, and the agentic work (Bid Proposal Agent) is still beta. Autodesk now frames AI as acting, which contradicts the earlier "has said less about it" read. Whether Autodesk is behind Procore on agents is not assessed here (Procore premise is not checked in this profile).

## 4. Product overlap with ProcurePro

- Inferred (assumption): Covers well: Tenders, Vendor Management, prequalification. Premise: Autodesk lists bid management, bidder invitations, and TradeTapp qualification (see sections 1 and 3).
- Observed: Autodesk says BuildingConnected lets users "Compare bids “apples to apples” and choose the best subcontractor for every project." (https://construction.autodesk.com/products/buildingconnected/)
- Inferred (assumption): Covers partially: Compare & Recommend. BuildingConnected offers bid comparison (Observed above) and the Forma Bid Bid Proposal Agent extracts inclusions and exclusions, but priced line-item scope comparison against estimates is announced as coming, not shipped.
- Observed: Autodesk says Forma Build Cost Management will let teams "create contracts in Cost Management in Forma Build from awarded bids" (https://web.archive.org/web/2026/https://www.autodesk.com/blogs/construction/autodesk-university-2026-forma-product-highlights-across-the-construction-lifecycle/) (the "Contracts" gap in ProcurePro's favour is narrower than the earlier draft said)
- Inferred (assumption): Does not cover: Procurement Schedule, Scope of Works Library, Lessons Learnt as ProcurePro defines them (searched construction.autodesk.com BuildingConnected and TradeTapp pages, the AU 2026 Forma blog and the APS developer blog for "procurement schedule", "scope of work", "lessons learnt", 2026-10-10; none found, but absence from marketing pages is not proof).
- Inferred (assumption): the overlap is real on the front half of the funnel (find and qualify bidders) and thin on the back half (compare priced scope, award, contract), but the back half is where Autodesk is now building.

## 5. Market position and geography

- Inferred (assumption): **North America:** dominant. This is the incumbent ProcurePro's US entry has to work around. Premise: the 2020 Autodesk release cited above puts the North American network at over one million professionals; no current third-party market share figure was found (searched Autodesk and general web, 2026-10-10).
- Observed: Autodesk announced on 13 October 2020 that "the BuildingConnected solution is now available in the United Kingdom, Ireland, Australia and New Zealand" (https://www.nasdaq.com/press-release/autodesk-expands-buildingconnected-into-emea-and-apac-to-give-global-construction)
- Observed: the construction.autodesk.com BuildingConnected page offers regional site selection for United Kingdom, Europe, Australia, New Zealand and others (https://construction.autodesk.com/products/buildingconnected/)
- Observed: Payapps operates as "Payapps in Australia, New Zealand, the U.K. and Ireland, and GCPay in North America" per Autodesk (https://adsknews.autodesk.com/en/news/autodesk-to-acquire-payapps/)
- Inferred (assumption): in Australia and the UK the BuildingConnected network is much thinner than in the US. Premise: no AU/UK network size figure was found (searched Autodesk pages and web for BuildingConnected Australia network size, subcontractors, 2026-10-10). This is the weakest premise in the profile; the 2020 launch means it is not a cold start, only unmeasured. The Forma Bid beta is US-region only per the APS blog.

## 6. Pricing & packaging

- Observed: Autodesk does not publish BuildingConnected pricing; a rival vendor blog (Down to Bid, a competing bid tool) reports "$3,600-$5,000+ annually with custom quotes based on size, users, geography", and says some subcontractors report cost tied to annual revenue (vendor-sourced, not Autodesk) (https://web.archive.org/web/2026/https://downtobid.com/blog/how-much-does-bid-board-pro-cost)
- Observed: the same Down to Bid blog says BuildingConnected "has a free entry-level tier for basic features, but the robust 'pro' features cost extra" (https://web.archive.org/web/2026/https://downtobid.com/blog/how-much-does-bid-board-pro-cost)
- Inferred (assumption): a free tier for subcontractors is the network play (the free entry tier is stated only by a rival vendor's blog; Autodesk's pages send pricing elsewhere, could not confirm on 2026-10-10). Autodesk subsidises the supply side to keep the graph dense, then charges the GCs who need to search it.

## 7. Differentiators vs ProcurePro

- Inferred (assumption): the network. In the US a GC can find and qualify subcontractors they have never worked with, which ProcurePro cannot offer on day one. Premise: Autodesk's "largest crowdsourced network" claim (vendor claim, section 2).
- Observed: Autodesk describes TradeTapp as "a prequalification and risk management software that allows vendors to submit qualification applications and general contractors to evaluate vendor risk." (https://web.archive.org/web/2026/https://construction.autodesk.com/products/tradetapp/)
- Inferred (assumption): financial risk data on subcontractors, via TradeTapp, is a capability ProcurePro does not have (premise: the TradeTapp description above; ProcurePro absence per reference/product-info.md).
- Observed: Autodesk's TradeTapp page says "Get multiple solutions at one price to manage bids, boost estimate accuracy, and qualify subs." (https://web.archive.org/web/2026/https://construction.autodesk.com/products/tradetapp/)
- Inferred (assumption): single-vendor consolidation for firms already standardised on Autodesk (premise: the bundle line above).

## 8. Risks for ProcurePro

1. Inferred (assumption): **US entry meets a dense network ProcurePro cannot match.** Highest likelihood. Buying decisions in US preconstruction default to BuildingConnected (no source; a judgement).
2. Inferred (assumption): **Forma Bid deepens down-funnel.** Autodesk already has a Bid Proposal Agent (Beta) extracting exclusions and says estimate-line-item and scope-gap comparison is coming soon, and contract creation from awarded bids. This is moving toward ProcurePro's core faster than the August read.
3. Inferred (assumption): **Payapps ownership.** Autodesk owns Payapps (SEC 10-Q) and shipped a Forma Build + GCPay integration (blog updated 20 May 2026), so it can bundle procurement to payment and squeeze the integration story ProcurePro could otherwise tell.
- Observed: Autodesk's blog says "Build now supports two paths for accounting and ERP integration", including a new "Cost Management in the Middle" model with GCPay (https://web.archive.org/web/2026/https://www.autodesk.com/blogs/construction/autodesk-forma-build-gcpay-a-new-integration-connecting-field-and-finance-is-here/)

## 9. Opportunities for ProcurePro

- Inferred (assumption): Autodesk's data answers "who should bid". ProcurePro's answers "is this price and scope right". Positioning against the network rather than trying to build one is the cheaper fight. Weaker than before, given the Bid Proposal Agent.
- Inferred (assumption): BidLevel (ProcurePro: reads supplier quotes and extracts pricing plus exclusions, per reference/product-info.md) overlaps with Autodesk's Bid Proposal Agent Beta, so "BidLevel does something Autodesk has not shipped" holds only as GA versus beta (searched Autodesk blog, APS blog, BuildingConnected help for GA agentic bid analysis, none found, 2026-10-10).
- Inferred (assumption): outside North America the network advantage is thinner, which favours ProcurePro in the UK and Middle East. Premise: Autodesk offers BuildingConnected in the UK and ANZ since 2020 (Observed, section 5); Middle East presence not checked.

## 10. Open questions

- Inferred (assumption): when does Forma Bid GA, and does it reach Australia and the UK? The beta is US-region only today (APS blog, April 2026).
- Inferred (assumption): does the promised Forma Estimate to bid package linking ship, and does it include scope-gap detection? This is the single most important thing to watch.
- Inferred (assumption): is Autodesk training models on the bid graph, or only using it for retrieval and recommendation? Autodesk says only that "Some Autodesk AI-powered features do not leverage machine learning and so do not require data for training of the underlying models" (Observed, section 2); no feature-level answer found.
- Inferred (assumption): what is Autodesk's plan for Payapps/GCPay relative to procurement workflows, beyond the Forma Build integration?
