# Dashboard copy voice

The writing standard for every HTML dashboard this project produces, alongside `dashboard-design.md`'s visual rules. These dashboards ship publicly, so the copy needs to read like a person wrote it, not like a model did. `check.py` only catches em dashes mechanically; everything else here needs a deliberate pass, both while drafting Tab 1's copy and again during design review.

## The tells to cut

**Em dashes.** Already gated by `check.py`, but also watch for a spaced hyphen or en dash standing in for one; same tell, different keyboard.

**Contrastive parallelism as a reflex.** "X, not Y", "not just X", "isn't X, it's Y". One clean use in the whole page can land; four or five means it's become the default sentence shape instead of an actual choice. Count them before calling copy done. Definitional uses are exempt (a legend that says "dotted underline = inferred, not observed" is labeling two states, not reaching for a rhetorical trick), but the same phrase turning up in every card's "implication" line is the tell.

**Fragment headlines built for punch.** "The pattern, not the fact." "Five names, two owners." Terse noun-phrase pairs with no verb read like a deck or a LinkedIn hook. A headline should be a sentence that says something specific: "Fleet-owned car sharing keeps failing the same way," not "The pattern, not the fact."

**Intensifier tics and grandiose absolutes.** Cut repeated "genuinely," "actually" (when it's doing emphasis rather than distinguishing a real figure from an estimate), "the single biggest," "almost no one," "the actual question." If a claim needs an intensifier to land, the claim is underspecified; make it more concrete instead.

**The rule-of-three reflex.** Not every list is three balanced items. If the underlying content naturally gives four findings or five recommendations, let it be four or five. Don't trim or pad to hit three.

**Symmetric bullets.** Vary sentence length and internal structure inside a list so items don't march in lockstep. A strengths/gaps grid can still have three items a side if that's what the analysis actually found; just don't let all three follow the identical "Bold label, one clipped sentence" shape.

**Compressed contrasts instead of dramatised ones.** "Brand-building runs through partnerships, not sponsorship" tells the reader there's a contrast. "Brand-building runs through Toyota Financial Services and an energy company's marketing budget" shows it, and reads like something a person actually found rather than a template filling in a blank.

**Sentences that are too short.** This is the clearest single difference between copy that reads generated and copy that reads written. A stack of short declaratives, each landing its own beat, is deck grammar: "The lane is open. The hard part is filling it." Aim for a mean past 90 characters a sentence across the page, with subordinate clauses and conjunctions doing the joining. Three things to look for: verbless fragments ("Founded in Auckland in 2007." or "Credible, crowded, and aimed past the buyer."), which should hang off a real subject and verb; related sentences sitting side by side without an "and", "so" or semicolon between them; and punchy codas, a short thumping line added after a paragraph that had already landed ("That is the story a launch can tell in one line."), which should be cut or folded in.

**Chains, when lengthening.** The fix for clipped prose has its own failure mode: every sentence turning into ", so ..., and ..." or three matching clauses ("owns its fleet, works from agency counters, and has built trust on..."). Join where the ideas are connected, and leave two unrelated facts as two sentences. Re-read anything you lengthened for a claim that shifted in the joining; a merged sentence can quietly say something the source doesn't.

## What to do instead

- Name the specific thing instead of the abstract category. "The lane is open, but building host supply from zero is the hard part" beats "this is a genuine opportunity."
- Let a plain phrase repeat if it's carrying real information (the "trust bar" concept recurring across two sections is fine; it's a thread, not a tic).
- Vary sentence length on purpose. A stack of short declaratives each landing its own beat is deck grammar; real prose runs a mix, with some sentences going past a comma and a subordinate clause.
- Read the whole page as prose once, out loud if useful, before calling it done. If the workspace's `voice-check.py` is available, run it over the page's prose too; it counts sentence length and the contrast patterns, which a read-through tends to miss. If a line would sound strange said to a colleague, rewrite it.

## Where this applies

Tab 1's narrative copy: the headline, executive-summary findings, cluster-card prose and implications, positioning strengths/gaps, and recommendations. Tab 2's procedural section labels ("The process," "Trust boundary") are documentation, not persuasive copy, and don't need the same treatment; don't force punchy rewrites onto plain process labels. Fixed wording mandated elsewhere in this project (for example the "re-checked against the pages they cite, not verified true" line) stays as specified even if it technically matches a pattern flagged above; a standing rule beats a style preference.
