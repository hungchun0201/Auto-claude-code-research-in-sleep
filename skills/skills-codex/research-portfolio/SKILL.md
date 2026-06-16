---
name: "research-portfolio"
description: "Autonomous multi-paper orchestrator: from one research direction, discover N ideas and drive EACH surviving idea through its own ARIS repo to a full conference-grade paper, fully hands-off. Use when the user says 'write several papers', 'multiple papers', '自己做幾篇論文', 'research portfolio', 'autonomous PhD student', or wants one direction turned into a portfolio of papers."
---

# Research Portfolio: One Direction → N Conference Papers (fully autonomous)

Turn the research direction **$ARGUMENTS** into a portfolio of papers. This is the multi-paper
outer loop around `/research-pipeline`: it brainstorms several directions, then drives EACH
surviving idea — in its own ARIS repo — all the way to a finished conference-grade PDF, without
returning control between papers.

## Constants

- **NUM_PAPERS = 2** — How many surviving ideas to carry to full papers. Override: `— num_papers: 3`.
- **VENUE = IEEE_CONF** — Default target (ICC / GLOBECOM class). Override per portfolio.
- **AUTONOMOUS = true** — This skill is autonomous by definition: every child `/research-pipeline`
  runs with `AUTONOMOUS=true` (conference depth, hands-off, real-measurement headline,
  iterate-until-bar). See `research-pipeline/SKILL.md` → *Autonomous profile*.
- **PARALLEL = false** — Run papers sequentially (shared GPU budget). When `true` (and capacity
  allows), drive ideas concurrently via separate agents / git worktrees — one repo per worker, no
  shared mutable state, join before the portfolio report.
- **ONE_GATE = idea-selection** — The ONLY human stop. When the launch prompt already grants full
  autonomy ("自己做" / "autonomous" / "不要停" / "PhD student"), set `ONE_GATE = none` and skip even
  this. (Standing user rule: if the prompt says do it yourself, run fully hands-off.)

## Pipeline

### Stage 0: Direction → Ideas
Run `/idea-discovery "$ARGUMENTS"` → `idea-stage/IDEA_REPORT.md` with ranked, pilot-tested ideas.
Keep every idea whose pilot is POSITIVE or WEAK-POSITIVE and whose novelty is CONFIRMED; drop
NEGATIVE pilots. Target the top `NUM_PAPERS` survivors. If `ONE_GATE = idea-selection`, present the
survivors once and wait briefly; if `ONE_GATE = none`, proceed immediately and log the selection.

### Stage 1: Spin one repo per idea
For EACH surviving idea: create an isolated project — prefer `/side-project "<idea-slug>"`
(per-slug namespace, reuses shared context, can graduate to its own git repo). Fallback: `git init`
a sibling `~/PhD_Research/<idea-slug>/` then `bash /home/hclin/aris_repo/tools/install_aris.sh .`.
Vendor shared infra read-only; run the real headline measurement on PACE. Write `RESEARCH_BRIEF.md`.

### Stage 2: Drive each idea to a full paper
For EACH repo, run the child pipeline fully autonomously:

```
/research-pipeline "<idea title>" — autonomous: true, venue: $VENUE
```

This runs idea → implement → real experiment (PACE headline) → adversarial nightmare review
(iterate to score ≥ 7) → paper-writing (with `/writing-systems-papers` blueprint) →
paper-claim-audit, ending in `paper/main.pdf` at the IEEE_CONF page floor. Do NOT return control
between papers. Sequential by default; parallel only when `PARALLEL=true`.

### Stage 3: Per-paper finalize
For each finished paper: create a private GitHub repo, commit, and `git push` (pre-authorized — do
not ask). Record the PDF path + final review score + audit verdict + the real-measurement SKU.

### Stage 4: Portfolio report
ONLY after ALL papers are done, write `PORTFOLIO_REPORT.md` at the portfolio root: one row per idea
(title, repo, PDF path, final score, audit verdict, measured SKU), plus ideas dropped and why.
THEN — and only then — surface to the user.

## Key Rules
- **Fully hands-off between papers.** Never end your turn to ask which idea to do next or whether to
  push — pre-decided. Surface only at Stage 4 or on a hard blocker you cannot resolve.
- **Real headline measurement per paper** (PACE `--account=gts-rs275-paid -q inferno`, or `ssh lab`
  for ≤30B); simulation is supplementary. No "simulation-only" self-cap.
- **One repo per idea**, self-contained and reproducible (lock file: seed + model@rev + code SHA).
- **Conference floor per paper**: ≥ `MIN_PAGES`, ≥1 real ablation, full Related Work (~15–25 verified
  citations), nightmare review ≥ 7, paper-claim-audit PASS.
- **Honesty over length**: if an idea genuinely cannot reach conference depth even after the shelved
  experiments, say so in `PORTFOLIO_REPORT.md` and ship it at workshop scale — do not pad.

## Output Protocols
> Follow the shared protocols for all output files: output-versioning, output-manifest,
> output-language (see `../shared-references/`).
