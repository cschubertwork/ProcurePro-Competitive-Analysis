# generate-analysis

Generate cross-competitor analysis reports on any topic from existing competitor profiles.

## Triggers

- `/generate-analysis <topic>` - Generate a full analysis report
- `/generate-analysis --list` - List previously generated analyses
- Natural language questions implying cross-competitor comparison (e.g., "How does everyone handle pricing?", "What does the integration landscape look like?", "How do we stack up on enterprise features?")

## Natural Language Detection

When the user asks a question that implies cross-competitor comparison, confirm before generating:

> "That sounds like a cross-competitor analysis on **[detected topic]**. Want me to:
> - **Full report** - Analyze all profiles and write a report to `analysis/`
> - **Quick summary** - Give you a conversational answer right here (no file output)"

Only proceed after the user chooses. This prevents accidental report generation from casual questions.

## Prerequisites

Before starting, verify these exist in the project root:

1. `reference/product-info.md` - the user's product context
2. `reference/competitors.md` - list of tracked competitors
3. `profiles/` directory with at least some populated competitor profiles

If profiles are mostly empty stubs (the majority have only headings with no substantive content), suggest:

> "Most profiles haven't been populated yet. Run `/competitive-update --all` first to research your competitors, then come back for analysis."

If `reference/product-info.md` or `reference/competitors.md` is missing, stop and tell the user what's needed.

## Process: Full Report

### Step 1 - Scope the Analysis

1. Read `reference/product-info.md` for the user's product context and positioning
2. Read `reference/guidelines.md` for the profile section structure
3. Read all profiles in `profiles/` and assess data coverage for the requested topic
4. Identify which profile sections are relevant to the topic
5. Report coverage to the user:

> "Found relevant data in **[X]/[Y]** profiles for **'[topic]'**. [Z] profiles have limited or no data for this dimension."

If coverage is thin (fewer than half of profiles have relevant data):

> "Data is thin for this topic - only [X] of [Y] profiles have relevant information. Want me to:
> - **Proceed** with what we have (will note gaps)
> - **Research first** - run `/competitive-update` targeting the gaps before analyzing"

Wait for the user's choice before continuing.

### Step 2 - Extract and Compare

1. For each profile with relevant data, extract all claims related to the topic
2. Track which claims are **Observed** (sourced from public information) vs **Inferred** (assumptions or educated guesses) for confidence reporting
3. Normalize the data into comparable dimensions:
   - Identify the key sub-dimensions within the topic (e.g., for "pricing": model type, starting price, tier structure, transparency)
   - Map each competitor's data to these sub-dimensions
4. Identify patterns:
   - **Clusters** - Groups of competitors with similar approaches
   - **Outliers** - Competitors doing something notably different
   - **Gaps** - Dimensions where data is missing across multiple profiles

### Step 3 - Generate the Report

Determine the filename: `analysis/<topic-slug>.md` where topic-slug is the topic in lowercase with hyphens replacing spaces (e.g., `pricing-models.md`, `integration-ecosystem.md`, `enterprise-readiness.md`).

**If a file already exists at that path:** Do NOT overwrite it. Instead, add a dated update section at the top of the file (below the title) noting what changed since the last analysis. Preserve all prior content.

**If the file is new:** Create it with the following structure:

```markdown
# [Topic]: Cross-Competitor Analysis

*Generated: [YYYY-MM-DD] | Based on [X] of [Y] competitor profiles*

## Executive Summary

[3-5 bullet points. Lead with the most strategically important insight. Each finding must be actionable - not "competitors vary in pricing" but "most competitors charge per-user, creating an opening for usage-based pricing."]

## Comparison Matrix

| Dimension | [Competitor 1] | [Competitor 2] | ... | [User's Product] |
|---|---|---|---|---|
| [Sub-dimension 1] | [Value] | [Value] | ... | [Value] |
| [Sub-dimension 2] | [Value] | [Value] | ... | [Value] |

*Values marked with (i) are inferred assumptions, not confirmed observations.*

## Competitor Clusters

### [Cluster Name] (e.g., "Premium Enterprise", "Self-Serve Mid-Market")
- **Who:** [Competitor list]
- **Approach:** [What they have in common on this dimension]
- **Implication for [Product Name]:** [What this means competitively]

### [Cluster Name]
...

### Outliers
- **[Competitor]:** [What makes them different and why it matters]

## [Product Name] Positioning

Where [Product Name] sits relative to the landscape:
- **Strengths:** [Where the product leads or matches on this dimension]
- **Gaps:** [Where competitors are ahead]
- **Opportunities:** [Positioning moves suggested by the data]

## Data Confidence

- **Observed (sourced) claims:** [X]%
- **Inferred (assumption) claims:** [Y]%
- **Profiles with limited data for this topic:** [list]

## Open Questions

[Bullet list of data gaps and follow-up research needed to strengthen this analysis. For each gap, suggest specific actions like "/competitive-update --competitor [name]" to fill it.]
```

### Step 4 - Offer Export

After writing the report, ask the user:

> "Report written to `analysis/[topic-slug].md`. Want me to export it as HTML for sharing?"

If yes, generate a clean HTML version in `exports/[topic-slug].html` with:
- Professional styling (clean typography, bordered tables, muted color palette)
- Product name in the header
- Print-friendly layout
- Date and confidence indicators visible

Create the `exports/` directory if it does not exist.

## Process: Quick Summary

When the user chooses "Quick summary" from the confirmation prompt:

1. Run Step 1 (scope) and Step 2 (extract and compare) the same way as the full report
2. Present findings conversationally in chat - no file output:
   - Lead with the 2-3 most important takeaways
   - Include a simplified comparison table (highlights only, not the full matrix)
   - Note any significant data gaps
   - End with: "Want me to generate the full report for this? Run `/generate-analysis [topic]`"

## Process: --list

When invoked with `--list`:

1. Check if `analysis/` directory exists. If not, report "No analyses have been generated yet."
2. Read all `.md` files in `analysis/` (exclude any `updates/` subdirectory if present)
3. For each file, extract the title (first `#` heading) and generation date from the header metadata line
4. Present as a table:

> **Previously generated analyses:**
>
> | Report | Generated | Profiles Covered |
> |---|---|---|
> | [Title] | [Date] | [X]/[Y] |

If the directory is empty, report "No analyses found in `analysis/`. Run `/generate-analysis <topic>` to create one."

## Important Rules

- **Always anchor to the user's product.** Every analysis must answer "what does this mean for us?" - not just describe the landscape. Read `reference/product-info.md` to understand positioning.
- **Confidence transparency.** Always report the Observed vs Inferred ratio. Flag when conclusions rest heavily on assumptions.
- **No hardcoded topics.** This skill works with ANY topic the user provides. Adapt the sub-dimensions and comparison structure to fit the topic naturally.
- **Additive updates.** If an analysis file already exists, add a dated update section rather than overwriting. This preserves the history of how the landscape has evolved.
- **Suggest specific research.** When data is thin, actively suggest `/competitive-update --competitor <name>` for the specific competitors that need more data, rather than just noting gaps abstractly.
- **No em dashes.** Use hyphens (-) instead of em dashes per user preference.
- **Get approval before writing.** For the natural language trigger path, always confirm with the user before generating a report file. The `--list` flag and explicit `/generate-analysis <topic>` invocations do not need additional confirmation.