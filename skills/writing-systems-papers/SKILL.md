---
name: writing-systems-papers
description: "Section-by-section structural blueprint and reviewer rubrics for systems papers targeting OSDI, SOSP, NSDI, ASPLOS, EuroSys, MLSys, SIGCOMM, and MobiCom. Authors apply the per-section discipline rules; auto-review-loop applies the Reviewer Rubrics. Use when the user says \"写系统论文\", \"systems paper structure\", \"OSDI paper\", \"SOSP paper\", or asks for venue-aware structural guidance."
argument-hint: [venue-or-section]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Writing Systems Papers

Structural blueprint and reviewer rubric set for **$ARGUMENTS**.

## How to use this skill

| Role            | Action                                                                                               |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| Author agent    | Read `references/whole-paper.md` first, then the section file you are drafting. Apply §1–5 of each. |
| Reviewer agent  | Read `references/whole-paper.md` (X-rubric) and each section file's §6 Reviewer Rubric. Emit §7 YAML. |
| auto-review-loop| Loop the reviewer agent across all 9 rubric files (8 section files + typography) plus the whole-paper aggregator per round. |

## Section references

| Section          | File                              | Reviewer test                                                |
| ---------------- | --------------------------------- | ------------------------------------------------------------ |
| Whole paper      | `references/whole-paper.md`       | Cross-section consistency, universal bans, paragraph discipline, gestalt |
| Typography       | `references/typography.md`        | LaTeX overflow, table fit, equation breaking, identifier wrapping        |
| Abstract         | `references/abstract.md`          | "Can a stranger paraphrase the central claim after one pass?" |
| Introduction     | `references/introduction.md`      | "Important, hard, in scope, plausibly solved here?"          |
| Motivation       | `references/motivation.md`        | "Why doesn't a simpler baseline already solve this?"         |
| Design           | `references/design.md`            | "Is this principled, implementable, better-motivated?"       |
| Implementation   | `references/implementation.md`    | "Is this the implementation of a system or a tour of a directory tree?" |
| Evaluation       | `references/evaluation.md`        | "Do the experiments actually test the paper's claims?"       |
| Related work     | `references/related-work.md`      | "Is the novelty stated, scoped, and contrasted fairly?"      |
| Conclusion       | `references/conclusion.md`        | "Does the takeaway match what the evidence supports?"        |
| Venue table      | `references/README.md`            | Per-venue overrides (word count, appendix policy, etc.)      |
| Sources          | `references/sources.md`           | Canonical URLs for CFPs, writing guides, exemplar papers     |

## Page allocation (12-page systems paper)

| Section              | Pages    |
| -------------------- | -------- |
| Abstract             | 0.25     |
| §1 Introduction      | 1.5–2    |
| §2 Background/Motiv. | 1–1.5    |
| §3 Design            | 3–4      |
| §4 Implementation    | 0.5–1    |
| §5 Evaluation        | 3–4      |
| §6 Related Work      | 1        |
| §7 Conclusion        | 0.5      |

10-page MLSys: scale down §1 and §5 by 0.5 page each. See `references/README.md` for the per-venue table.

**6-page IEEE conference (ICC / GLOBECOM, references included)** — invoked when `/research-pipeline` passes `venue: IEEE_CONF`. Keep every section role, universal ban (U1–U10), and paragraph-discipline rule, but compress to ~6 pages: Abstract 0.2 · §1 Introduction ~1 · §2 Background/Motivation ~0.75 · §3 Design/Method ~1.5 · §4 Evaluation ~1.5 (setup → E2E → ≥1 ablation → scalability) · §5 Related Work ~0.5 · §6 Conclusion ~0.25 · References ~0.3. Structural rigor does not relax — only the prose budget does. Aim for ~15–25 verified citations even at 6 pages.

## Workflow

1. Confirm target venue and page cap (see venue table).
2. Read `references/whole-paper.md` (universal bans + paragraph discipline + X-rubric) and `references/typography.md` (LaTeX hygiene).
3. Draft each section with the matching `references/<section>.md` open. Apply §2 (required components), §3 (discipline rules), §4 (hard bans) while writing.
4. After each section is drafted, self-apply the §6 Reviewer Rubric of that section. Resolve every FAIL before moving on.
5. After all sections exist, apply the whole-paper X-rubric. Resolve every cross-section FAIL.
6. Hand off to `/paper-write` for LaTeX rendering and DBLP-based citation verification.
7. After every `pdflatex` run, grep `main.log` for `Overfull \hbox`. Treat warnings > 5pt as build errors (U10 / T8). Apply fix recipes from `references/typography.md` §2 until zero remain.
8. Optionally run `/auto-review-loop` for adversarial multi-round review.

## Universal hard bans (apply to every section)

| ID  | Banned pattern                                                                                  |
| --- | ----------------------------------------------------------------------------------------------- |
| U1  | Inline rhetorical-role labels in body text: `\paragraph{The problem}`, `\paragraph{The gap}`, `\paragraph{The thesis}`, `\paragraph{Contributions}`, `\paragraph{Roadmap}`, `\paragraph{Why}`, `\paragraph{What}`, `\paragraph{Tradeoff}`, `\paragraph{Named alternative}`. Section roles are paragraph functions, not headings. |
| U2  | More than two enumerated label series (e.g., G1–Gn AND O1–On AND R1–Rn AND M1–Mn AND Q1–Qn AND contributions 1–N) across the body. Enumeration discipline: at most two such series in the entire paper. |
| U3  | Comparison tables (in §6 or anywhere) that put accuracy/throughput/latency numbers from different workloads side by side. If the column is a measured number, all rows must come from the same workload. |
| U4  | Fabricated, hallucinated, or unverifiable citations. Every reference must resolve via DBLP, CrossRef, or the venue's proceedings page. |
| U5  | Any acceptance-critical claim that depends on appendix-only evidence at NSDI / MLSys / SIGCOMM / MobiCom; the main body must stand alone. |
| U6  | "We describe", "We discuss", "We present and evaluate" prose-table-of-contents phrasing in abstract, §1, or contributions. |
| U7  | Subsection-level "Why / What / Tradeoff / Named alternative" four-block templates appearing three or more times in §3. Mechanism rationale must be woven into prose, not announced. |
| U8  | The same statistic appearing in abstract, contributions, evaluation, and conclusion. A number belongs to its primary section. |
| U9  | File paths, filenames, function names, class names, struct names, JSON keys, configuration-knob names, CLI flag names, or shell commands in the body text of any section §1–§7. Components are named semantically. The appendix may include such identifiers when essential for reproducibility, capped at ≤ 8 distinct identifiers in the entire appendix. The body contains zero. |
| U10 | Any `Overfull \hbox` warning > 5pt in compiled `main.log`. See `references/typography.md` for LaTeX patterns that cause overflow and the fix recipes. |

A single U-trigger makes the round FAIL regardless of section-level scores.

## Paragraph discipline (universal)

`\paragraph{...}` is a legitimate LaTeX tool — what these rules forbid is *how* it is used, not whether. A `\paragraph{X}` label promises a developed paragraph that establishes, argues, and concludes one named idea. A 1- to 3-sentence paragraph under a `\paragraph{}` label is a *framework-question stub*; a stack of such stubs in one subsection reads as Q&A, not as argument.

**Permitted**: an occasional `\paragraph{X}` where `X` names a content-specific entity (a mechanism, regime, phenomenon, decision) and the paragraph develops it across ≥ 4 sentences. `\paragraph{Bandwidth-bound regime.}`, `\paragraph{Receiver-driven priority assignment.}` are fine.

**Banned**: a stack of `\paragraph{X_i}` blocks where each `X_i` is an abstract rubric question (Why / What / Tradeoff / Goal / Named alternative …) and each block answers in 1–3 sentences.

| ID  | Cat  | Rule                                                                                                |
| --- | ---- | --------------------------------------------------------------------------------------------------- |
| P1  | BAN  | A `\paragraph{}`-led paragraph contains fewer than 4 sentences.                                     |
| P2  | BAN  | Two consecutive body paragraphs are both `\paragraph{}`-led and each fewer than 5 sentences.        |
| P3  | BAN  | A subsection contains 3 or more `\paragraph{}`-led paragraphs each fewer than 5 sentences.          |
| P4  | BAN  | `\paragraph{X}` label `X` is an abstract rubric term (Why, What, How, Tradeoff, Goal(s), Non-goals, Approach, Method, Setup, Result(s), Conclusion, Limitation(s), Motivation, Discussion, Background, Overview, Architecture, Rationale, Named alternative, Alternative, …). Use content-specific labels only. |
| P5  | BAN  | Mean body paragraph length across the paper is fewer than 5 sentences or fewer than 100 words.      |
| P6  | DISC | `\paragraph{X}` labels name a content-specific entity in this paper.                                |
| P7  | DISC | Consecutive paragraphs are connected: each opens with a connective signal (pronoun back-reference, entity continuation, transition phrase). |
| P8  | DISC | Each topic sentence advances the argument; it is not a rephrased rubric question.                   |
| P9  | DISC | "Why / what / tradeoff" rhythms are integrated into 1–2 flowing paragraphs, not split into 3 labeled blocks. |

Full discipline, verification procedures, and YAML schema live in `references/whole-paper.md` §2.

## Academic integrity

- Never fabricate observations, traces, deployments, or experimental results.
- Never generate citations from memory. Use `/paper-write`'s DBLP → CrossRef → `[VERIFY]` chain.
- Disclose LLM use per venue policy.
- Limitations and failure regimes are first-class content, not appendix material.
