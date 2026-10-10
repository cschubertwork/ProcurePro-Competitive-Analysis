# Set completeness: who else a commercial head contractor could buy from

*Researched: 2026-10-10. Scope: businesses a commercial head contractor in ANZ, the UK or North America could buy for subcontractor procurement, tendering, bid levelling or trade-package comparison, live or dead. Desk research by web search and page fetches on 2026-10-10; vendor statements stay vendor claims.*

The five-company set (Autodesk, Procore, Felix, Causeway, Kojo) is a top-five brief, not a census. This file records what the set leaves out, whether each omission matters to the analysis, and which of them contradict the claim in `analysis/ai-data-moat-and-automated-workflows.md` that ProcurePro's corpus is "the only one sitting inside the moment project value is committed" and that "none of the other five sits in the room when a head contractor levels five quotes and picks one."

## Headline findings

- Inferred (assumption): the claim is **contradicted by two members of the set itself**. Autodesk's BuildingConnected page says "Compare bids “apples to apples” and choose the best subcontractor for every project." (https://construction.autodesk.com/products/buildingconnected/). Procore's bid management page says "Compare bids side-by-side with bid leveling . Once you've selected the best bid for the job, convert it into a subcontract or purchase order with the click of a button" (https://www.procore.com/bid-management). Both sit in the levelling and award step. What neither publishes is an AI scope-and-exclusion extraction claim of BidLevel's kind, so a narrower claim survives (see "What survives" below).
- Inferred (assumption): **E1 (EstimateOne) is the live player that most directly falsifies the claim**, in ProcurePro's home market, and it is not in the five. See entry 1.
- Inferred (assumption): a US wave of AI bid-levelling startups (Consight, Buildr, Bridgeline, Arctis, Trueleveler, EstimateHawk, Melt, Palcode) sells exactly the "extract, structure, compare" capability the analysis rates ProcurePro as leading at. None has a corpus of ProcurePro's published scale; that is a judgement from what each publishes (searched each vendor homepage, 2026-10-10).
- Inferred (assumption): the analysis line "Nobody credible is serving the head contractor's award decision with agentic depth" depends on "agentic depth"; on the narrower "serving the award decision" it is false (E1, Archdesk, Procore, Autodesk, Consight, Trueleveler all serve it).

## What survives of the claim

- Inferred (assumption): a defensible rewording is "the only corpus of awarded commercial terms (priced scope and exclusions) at 200,000-package scale that has been published". This rests on ProcurePro's own figures (product-info.md, being re-checked separately), and on not finding any competitor publishing an equivalent awarded-terms dataset (searched each vendor homepage and the AI bid-levelling search results, 2026-10-10). It is a negative, so one counter-example fails it.
- Inferred (assumption): E1 holds a plausibly larger tender-side dataset. E1 states "In 2025, Aussie Head Contractors posted 24,000 tenders at a total value of $354 billion!" (https://estimateone.com/about-us/), against ProcurePro's A$130bn across 6,000+ projects. Tendered value is not awarded value, but "narrowest corpus" and "only dataset" claims need a comparison with this figure.

## Live players

### 1. E1 (formerly EstimateOne) - ANZ, expanding UK. FALSIFIES the "only one" claim in ANZ
- What it does: tender platform connecting head contractors (builders), subcontractors and suppliers, with an AI quote comparison tool for head contractors.
- Observed: E1's help article says "Quote Analysis leverages AI to automatically read and compare two to five subcontractor or supplier quotes within a single trade package. By scanning for risks, discrepancies, and scope gaps in minutes" and is dated 13 April 2026, including analysis "against a Bill of Quantities" (https://builder.support.estimateone.com/en/articles/1756366327-quote-analysis)
- Observed: E1's resources page lists "Builder – AI-enabled quote analysis on E1", last updated Jan 21, 2026 (https://estimateone.com/resources/for-main-contractors/)
- Observed: E1 says "We are the market leaders in Australia and NZ and have expanded our team into the UK. Our growth accelerated in 2022 after securing investment from Potentia Capital and Saniel Ventures." (https://estimateone.com/about-us/)
- Observed: E1 says "more than 100,000 Australian organisations used our platform to manage the construction tendering process. In 2025, Aussie Head Contractors posted 24,000 tenders at a total value of $354 billion!" (https://estimateone.com/about-us/)
- Observed: E1 describes itself as "Australia’s leading construction tender platform" (https://estimateone.com/)
- Inferred (assumption): E1 acquired Dutch platform 12Build in January 2026 (press release dated 23 January 2026, reported in web search results from GlobeNewswire via Technology Magazine; the page returned no text to curl or Chrome on 2026-10-10, so this is not quote-verified)
- Reaches the award decision: partly. It compares quotes within a trade package before award; it does not (on the pages read) generate the contract. Inferred (assumption).
- Effect on the set: weakens the "only one inside the moment" claim, the "nobody credible is serving the award decision" bullet, and the "ProcurePro won at home" framing in the Autodesk bullet, since an Australian tender platform with the head contractors' send-outs also has AI levelling. **Rank 1 set gap.**

### 2. Procore Bid Management (inside Procore, already in set) - North America, global
- Observed: Procore's page says "Easily create, manage, level, and track bid invitations. Compare bids side by side to identify gaps and outliers" (https://www.procore.com/bid-management)
- Reaches the award decision: yes, including conversion of the chosen bid into a subcontract or purchase order (Observed, same page).
- Effect: contradicts the comparison table's "Automation depth: Agents that act" being the only relevant Procore descriptor, and the "none of the other five sits in the room" line. Not a missing company; a mis-stated one.

### 3. BuildingConnected (Autodesk, already in set) - US
- Observed: "Compare bids “apples to apples” and choose the best subcontractor for every project." (https://construction.autodesk.com/products/buildingconnected/)
- Reaches the award decision: yes (comparison and selection). Effect as for Procore.

### 4. Archdesk - UK and Australia (regions also US, Canada)
- What it does: construction management suite with a subcontractor tendering module.
- Observed: "Subcontractor Tendering Issue RFQs and compare supply chain quotes side by side" and region choices "Australia ... United States ... Canada ... United Kingdom" (https://archdesk.com/en-au)
- Inferred (assumption): live and selling in both ProcurePro's home market and its most developed expansion market. It was excluded in `competitors.md` as "residential, SMB"; that rationale looks stale.
- Reaches the award decision: yes, side-by-side compare before award (Observed above). Weakens the "none of the other five" line. **Rank 3 set gap.**

### 5. Consight - US (market not stated on homepage)
- Observed: "Consight helps estimators generate scopes, send bid invitations, automate bid leveling, and identify scope gaps [source has an em dash here] all in one preconstruction platform." and "$12B+ in project value managed on Consight" (https://home.consight.ai/)
- Reaches the award decision: yes (levelling and scope gaps). Vendor claim of $12B+ managed is the same shape as ProcurePro's A$130bn claim at about a tenth of the size. Home market: could not confirm on 2026-10-10.

### 6. Arctis AI - home market could not confirm
- Observed: a five-agent preconstruction platform with "04 Evaluate Level every bid." and "Every agent works from the same data foundation. Projects, bids, prices, and decisions flow into Arctis Intelligence, making every next process smarter." (https://arctisai.com/)
- Inferred (assumption): this is the clearest third-party statement of an award-data moat narrative and the clearest "agents that act" competitor to ProcurePro's gap. It claims a compounding corpus of "bids, prices, and decisions"; no scale figure published. **Rank 2 set gap on the moat claim.**

### 7. Trueleveler - home market could not confirm (priced in US dollars per Capterra)
- Observed: "Bid Leveling Compare up to 10 vendor quotes side-by-side against your RFQ." (https://www.trueleveler.com/)
- Inferred (assumption): Capterra lists a US$99 flat monthly starting price (search-result summary, not fetched), which also breaks the line that "nobody publishes pricing".

### 8. Buildr, Bridgeline, EstimateHawk, Melt (Meltplan), Palcode, Bidblox - US-style startups, 2024-2026
- Observed (Buildr): "AI reads every submitted PDF, pulls out line items, flags exclusions, and normalizes pricing into a side-by-side comparison automatically." (https://buildr.com/blog/ai-bid-leveling/)
- Observed (Bridgeline): "The precon co-pilot for SMB general contractors From architectural plans to award-ready contract in an afternoon, not days." and "levels every sub bid side by side, and generates the contract." (https://bridgeline.io/)
- Observed (EstimateHawk): page title "EstimateHawk: AI Bid Comparison & Bid Leveling Software" (https://www.estimatehawk.com/)
- Observed (Melt): "Bid Leveling Sub bids leveled, gaps flagged, apples to apples" (https://meltplan.com/)
- Observed (Palcode): "BidLevelingPal ... run the full bid management lifecycle: subcontractor ITB outreach, scope sheet generation, bid leveling, and post-award vendor onboarding." (https://palcode.ai/)
- Inferred (assumption): Bidblox is a 2024 startup per a directory listing (datadrivenaec.com via search); its own site returned no text, so not quote-verified.
- Reaches the award decision: yes for all (levelling before award; Bridgeline also generates the contract). Mostly SMB and sub-scale; threat is to the "BidLevel shipped capability" differentiation, not to the corpus claim. Inferred (assumption).

### 9. Oracle Aconex bid and tender management (Oracle BidContender) - Australia origin, global
- Observed: Oracle's Aconex page offers "A secure, central platform to manage tenders and bids Reduce manual input and complexity with a structured and consistent framework for the tendering process." (https://www.oracle.com/construction-engineering/aconex/)
- Observed: "Oracle to buy Australia's Aconex for $1.19 billion" (CNBC, 18 December 2017) (https://www.cnbc.com/2017/12/18/oracle-to-buy-australias-aconex-for-1-point-19-billion.html)
- Inferred (assumption): BidContender, an Aconex-origin tender tool, is listed on Capterra as Oracle BidContender with most customers in Australia (search-result summary of Capterra, aggregator); no Oracle page naming BidContender was found (searched oracle.com and web search, 2026-10-10), so treat it as legacy or folded into Aconex.
- Reaches the award decision: distribution and receipt of tenders and responses; no AI levelling claim found. ProcurePro lists an Aconex integration (https://procurepro.co/blog/procore-and-procurepro-are-better-connected). Weakens nothing directly; competitors.md lumped Oracle with ERP, which is a mislabel.

### 10. BidWork and Constructionline Tender Management (Once For All) - UK
- Observed: BidWork is "For main contractor estimators, surveyors and project managers looking for suppliers." with an "AI-powered X-ray tool" to "Extract scope items from tender packs", and lets users "distribute and track bill of quantities (BOQ) responses" (https://www.bidwork.co.uk/)
- Observed: Constructionline lists "Tenders and Supplier Sourcing" and "Tender Management Transform your tender management process" (https://www.constructionline.co.uk/)
- Inferred (assumption): BidWork and Constructionline share an owner or brand family (BidWork page references "Once For All", Constructionline site names "Once For All"). Not verified in Companies House.
- Reaches the award decision: stops at enquiry distribution and BOQ responses; no priced comparison claim read. UK main-contractor buyer and a live UK tender tool ProcurePro will meet. **Rank 4 set gap** (UK).

### 11. ConstructConnect (SmartBid, Bid Management, iSqFt) - North America
- Observed: "Manage & Win Bids SmartBid® Send ITBs & manage subs Bid Management Win bid day with confidence" and a "How We Compare" list naming Procore, PlanHub, Dodge Construction Network and BuildingConnected (https://www.constructconnect.com/bid-management)
- Reaches the award decision: bid management for the GC and sub side; no AI levelling claim read. Inferred (assumption): a direct incumbent for US head-contractor bid management beside BuildingConnected. Not in the five. **Rank 5 set gap** (US).

### 12. Pantera Tools - US
- Observed: "Budget-friendly bid and project management software made for Project Owners, General Contractors, and Subcontractors." (https://www.panteratools.com/)
- Inferred (assumption): despite the brief's "UK tender portal" framing, no UK specific offer was found; listings are US-oriented (searched "Pantera Tools tender management construction UK", 2026-10-10). Invitation-to-bid and prequalification; no levelling claim found.

### 13. Buildertrend - US, residential (excluded in competitors.md)
- Observed: its bidding page says "compare responses side-by-side and select the best option faster" (Wayback capture) (https://web.archive.org/web/2026/https://buildertrend.com/financial-tools/construction-bidding-software/)
- Inferred (assumption): marketed to home builders and remodelers; not a commercial head-contractor award tool. Exclusion stands.

### 14. Jaggaer - global, cross-industry source-to-pay
- Observed: sourcing page lists "Commercial & technical bid envelopes", "Multi-criteria evaluation & BAFO rounds" and "Side-by-side scenario sensitivity analysis What-if modelling pre-award" (Wayback capture) (https://web.archive.org/web/2026/https://www.jaggaer.com/solutions/sourcing)
- Inferred (assumption): serves capital-project owners and large contractors via enterprise sourcing; no trade-package scope levelling found (searched Jaggaer construction and bid-levelling, 2026-10-10). Reaches award in a generic sense. Low relevance to the claim.

### 15. TenderLink (illion) - ANZ, tender notification and e-tender box
- Observed: TenderLink says it provides "contract awards and procurement activity from one platform" and covers "hundreds of industries" (https://illion.tenderlink.com/)
- Inferred (assumption): a notification and tender-box service for public and private work; not a levelling tool. Does not reach the award decision in the sense of priced comparison.

### 16. iTWO tender (RIB Software) - Germany-centred bidder portal
- Observed: RIB's own page refers to "der Bieterplattform iTWO tender von RIB" (bidder platform) (https://www.rib-software.com/en/rib-itwo-tender)
- Inferred (assumption): the bidder side of public procurement, German market; not a head-contractor trade-package comparison tool. Does not weaken any claim.

### 17. Plantcraft
- Inferred (assumption): no business called Plantcraft in construction procurement was found (searched "Plantcraft construction software", 2026-10-10). The nearest match is Plancraft, a German SMB trades software company (quoting, invoicing, GAEB import), not a head-contractor procurement tool. Not a gap.

## Dead or absorbed

- Observed: Payapps is now Autodesk-owned (10-Q, Feb 2024) (https://www.sec.gov/Archives/edgar/data/769397/000076939724000091/adsk-20240430.htm); payments, not procurement.
- Inferred (assumption): no dead procurement-for-contractors company was surfaced beyond Aconex's BidContender legacy brand; the search was not designed to find defunct startups (searched "BidContender", "Pantera Tools", AI bid-levelling queries only).

## Where the five set is exposed, ranked

1. **E1 (ANZ, UK, now Netherlands).** Live, AI quote comparison for head contractors since early 2026, 24,000 head-contractor tenders in 2025. Contradicts "only one", "nobody credible", and the ANZ comparison cells.
2. **Arctis AI (home market unconfirmed).** States an award-data moat narrative with agents. Matters because the analysis rates ProcurePro "one rung behind" on agents.
3. **Archdesk (UK, AU).** Live subcontractor tendering with side-by-side compare; excluded on a stale rationale.
4. **BidWork / Constructionline (UK).** Live UK main-contractor tender tooling with an AI X-ray tool.
5. **ConstructConnect (US).** Incumbent for US head-contractor bid management; not in the set.
6. **AI levelling startups (Consight, Trueleveler, Buildr, Bridgeline, Melt, Palcode, EstimateHawk).** Individually small; together they erode "BidLevel" as a differentiator in the US.
