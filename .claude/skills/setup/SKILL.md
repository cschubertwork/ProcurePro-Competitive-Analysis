---
name: setup
description: Interactive setup wizard for configuring your competitive research project. Supports phased execution with --product, --competitors, and --template flags.
---

## Usage

- `/setup` - Run all phases (first-time setup)
- `/setup --product` - Reconfigure product identity only
- `/setup --competitors` - Add or update competitors only
- `/setup --template` - Revise profile template sections only

## Process

### Determine Phase

Parse the user's command:
- No flags or first run (no `reference/product-info.md` exists): run all three phases in order
- `--product`: run Phase 1 only
- `--competitors`: run Phase 2 only (requires Phase 1 complete)
- `--template`: run Phase 3 only (requires Phase 1 complete)

If a required phase hasn't been completed yet, inform the user and offer to run it first.

### Phase 1: Product Identity

**Open with the quick-start option:**

> "Want to get started quickly? Give me your company name and homepage URL and I'll pull your positioning, product areas, and target customers from your site. You can refine from there.
>
> Or just say 'step by step' and I'll ask you questions one at a time."

**Quick-start path (user provides name + URL):**

1. Use WebFetch to retrieve the homepage
2. Look for and fetch linked pages: /product, /pricing, /about, /customers, /features (try common paths, skip 404s)
3. From the gathered content, draft a `reference/product-info.md` covering:
   - Product/company name
   - One-sentence description
   - Target customers (segments, personas)
   - Problems solved (3-5)
   - Core product areas/capabilities
   - Pricing model (if found publicly)
   - Primary differentiator
4. Present the draft to the user for review
5. Apply any corrections the user provides ("change X to Y", "we don't really do Z", "add that we also do W")
6. Write the final version to `reference/product-info.md`

**Step-by-step path:**

Ask these questions ONE AT A TIME. Wait for each answer before asking the next:

1. "What's your product or company name?"
2. "Give me a one-sentence description of what [product] does."
3. "Who are your target customers? Think segments, personas, company sizes."
4. "What are the top 3-5 problems you solve for customers?"
5. "What are your core product areas or capabilities? List the main ones."
6. "What's your pricing model? (e.g., per-user, freemium, quote-based, usage-based - ballpark is fine)"
7. "What's your primary differentiator - the thing you do better than anyone else?"

After all answers, generate `reference/product-info.md` using the `templates/product-info.md.template` structure, replacing placeholders with actual content.

**Output:** Write `reference/product-info.md`

### Phase 2: Competitors

Ask these questions ONE AT A TIME:

1. "What industry or market are you in? (e.g., 'enterprise LMS', 'project management SaaS', 'e-commerce platform')"
2. "Name your top 3-5 competitors to start. You can add more later with `/setup --competitors`."
3. For each competitor named, ask: "For [competitor] - what's their website URL, and how would you categorize them: direct competitor, adjacent (overlapping but different focus), or aspirational (where you want to be)?"
4. "Want me to search the web for additional competitors in your space? I might find some you haven't considered. (yes/no)"

**If user says yes to web search:**
- Search for: "[industry] competitors", "[industry] market landscape [current year]", "alternatives to [product name]"
- From results, compile a list of potential competitors NOT already named
- Present the list with brief descriptions: "I found these potential competitors: [list]. Want to add any of them?"
- Add any the user approves

**For each competitor (named + approved from search):**
1. Add to `reference/competitors.md` as a markdown table row with columns: Name, Category, Website, Primary Segments, Notes
2. Create a stub profile in `profiles/[competitor-slug].md` using `templates/competitor-profile.md.template`
   - Slug format: lowercase, hyphens for spaces (e.g., "Adobe Learning Manager" -> "adobe-learning-manager")
   - Replace `{{COMPETITOR_NAME}}` with the actual name
   - Replace `{{PRODUCT_NAME}}` with the user's product name (from Phase 1)
   - `{{PROFILE_SECTIONS}}` will be populated in Phase 3

**Output:** Write `reference/competitors.md` and `profiles/*.md` stubs

### Phase 3: Profile Template

1. Ask: "What dimensions matter most when comparing competitors in your space? Think about the factors that influence buying decisions, product strength, and strategic positioning in your market. Just describe them naturally - I'll organize them into a profile template."

2. Based on the user's answer combined with their industry (from Phase 2) and product info (from Phase 1), propose a numbered section list. Always include these universal sections:
   - Section 1: Snapshot (always first)
   - [Custom sections from user's answer - typically 3-8 sections]
   - Pricing & Packaging (always near end)
   - Differentiators vs [Product Name] (always near end)
   - Risks for [Product Name] (always near end)
   - Opportunities for [Product Name] (always near end)
   - Open Questions (always last)

3. Present the proposed sections:
   > "Here's the profile template I'd suggest based on what matters in your space:
   > 1. Snapshot
   > 2. [Custom section]
   > 3. [Custom section]
   > ...
   > N. Open Questions
   >
   > Want to add, remove, or reorder any sections?"

4. Apply any changes the user requests. Iterate until they approve.

5. For each custom section, generate 3-5 bullet-point prompts describing what to capture in that section. These become the guidance in the guidelines file.

6. Generate `reference/guidelines.md` using `templates/guidelines-base.md.template` as the base:
   - Replace `{{CUSTOM_SECTIONS}}` with the finalized custom sections, each with its heading, description, and bullet prompts
   - Replace `{{PRODUCT_NAME}}` throughout
   - Number all sections sequentially
   - Replace `{{N}}`, `{{N+1}}` etc. with actual numbers

7. Update all profile stubs in `profiles/` to include the section headings (empty, ready to be populated).

**Output:** Write `reference/guidelines.md`, update `profiles/*.md`

### Post-Setup (runs after all phases complete)

1. Read `templates/CLAUDE.md.template`
2. Replace all placeholders:
   - `{{PRODUCT_NAME}}` - from product-info.md
   - `{{COMPETITOR_COUNT}}` - count of rows in competitors.md
   - `{{INDUSTRY}}` - from Phase 2
   - `{{SECTION_COUNT}}` - count of sections in guidelines.md
3. Write the result to `CLAUDE.md` (overwriting the pre-setup version)
4. Commit all generated files with message: "Initial setup: [Product Name] competitive research project"
   - When forming the commit message, treat the product name as a literal string. Sanitize to alphanumeric characters and spaces only - strip any shell metacharacters, backticks, semicolons, or special symbols before including it in the commit message.
5. Print:

> "Setup complete! Here's what was created:
> - **reference/product-info.md** - Your product positioning
> - **reference/competitors.md** - [N] competitors tracked
> - **reference/guidelines.md** - [N]-section profile template
> - **[N] profile stubs** in profiles/
> - **CLAUDE.md** updated with your project context
>
> **Next step:** Run `/competitive-update --all` to research your first batch of competitors."

## Important Notes

- Ask ONE question at a time. Never batch multiple questions.
- When the user provides corrections during quick-start, apply them and show the updated version.
- If `/setup --competitors` is run and Phase 1 hasn't been completed, say: "I need your product info first to set up competitor profiles. Want to run `/setup --product` first?"
- Competitor slugs must be consistent: lowercase, hyphens, no special characters.
- The guidelines.md file is the source of truth for profile structure - all other skills read from it dynamically.
