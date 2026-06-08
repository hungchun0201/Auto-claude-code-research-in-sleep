# Abstract — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

The abstract is the only piece of writing many readers will ever see. It must transmit, in one paragraph, the central claim, the core mechanism, and one decision-relevant number to a broad systems reader who will read no further. The abstract is also the basis for reviewer assignment and online-database memory; placeholder or trivial abstracts are desk-rejected at OSDI and MobiCom.

The abstract is a paragraph, not a list of fragments. It reads as continuous prose. Each rhetorical role below is performed by a sentence (or by sentences merged together), not announced by a label.

## 2. Required components

| ID  | Cat  | Component       | Content the sentence(s) must carry                                                                          |
| --- | ---- | --------------- | ----------------------------------------------------------------------------------------------------------- |
| A1  | COMP | Motivation      | Why the area matters: quantified pressure, importance, or impact in concrete domain terms.                  |
| A2  | COMP | Problem         | The specific problem and its scope (one-system, cross-system, regime).                                      |
| A3  | COMP | Approach        | The system or method name, plus the one-line characterization of how it works.                              |
| A4  | COMP | Result          | The strongest single quantitative outcome with the baseline it is measured against.                         |
| A5  | COMP | Implication     | What the result implies; whether it is general, generalizable, or case-specific.                            |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| A6  | DISC | Target 180 words; hard cap depends on venue (OSDI / NSDI / MLSys ≤ 220; SIGCOMM ≤ 200; MobiCom ≥ 100, ≤ 220). |
| A7  | DISC | Total distinct numeric values in the abstract: ≥ 1, ≤ 3. Every additional metric belongs in §5.               |
| A8  | DISC | No figure, no table, no citation marker `[N]`, no forward reference (`§3`, `Figure 2`, `Table 1`).            |
| A9  | DISC | Every acronym expanded on first use, including system names if non-obvious (vLLM, MAPE, SKU, NUMA, etc.).     |
| A10 | DISC | The abstract is one continuous paragraph. No `\paragraph{...}` labels, no inline rhetorical-role markers, no bullet lists. |
| A11 | DISC | Achievement verbs only: *show, reduce, achieve, match, eliminate, sustain*. Effort verbs are banned: *investigate, explore, study, work on*. |
| A12 | DISC | Title, abstract, and §1 contribution paragraph state the same central claim in different words. The central concept name (system / mechanism / claim) appears verbatim in all three. |
| A13 | DISC | The abstract states the central claim in a single sentence — the *thesis sentence*. The reader can underline one sentence that, on its own, communicates the contribution. |

## 4. Hard bans

A single trigger forces section pass = false.

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| A14 | BAN | More than 3 distinct numeric values in the abstract.                                                        |
| A15 | BAN | Vague magnitude words without numbers: *very, significant, substantial, dramatic, considerable, marked*.    |
| A16 | BAN | Forward references or inline citation markers in the abstract text.                                         |
| A17 | BAN | Prose-table-of-contents phrasing: "We describe / discuss / present and evaluate / show how to build…".     |
| A18 | BAN | Two competing primary claims. The story bifurcates.                                                         |
| A19 | BAN | The abstract is split into labeled fragments (`\paragraph{The problem}`, `\paragraph{The gap}`, `\paragraph{The thesis}`, etc.). |
| A20 | BAN | The abstract contains training/test split numbers, ablation breakdowns, per-cell statistics, or held-out percentages. These belong in §5. |

## 5. Worked exemplar (Homa, SIGCOMM 2018)

Homa's abstract is one paragraph that lands on one quantified claim. Reading it sentence by sentence:

1. Workload pressure — short-message datacenter traffic suffers tail latency under high load.
2. Gap — existing transports optimize throughput, not short-message tail latency.
3. Approach — a receiver-driven, priority-managed transport.
4. Result — sub-15 µs 99th-percentile RTT at high load.
5. Implication — short-message workloads need transport designed around their tail.

Observe what the paragraph does *not* contain: no inline labels, no second number, no citation, no forward reference, no `Figure N`. The verbs are *uses, achieves, reduces*. The paragraph can be paraphrased in a single sentence: *Homa is a receiver-driven priority-managed transport that delivers sub-15 µs p99 RTT on short messages at high datacenter load.*

When drafting your own abstract, do not copy Homa's wording. Read for rhythm and discipline, then write your own paragraph.

## 6. Reviewer Rubric

Apply each row Y/N from the abstract text alone. Do not infer from later sections.

**Pass = every COMP and DISC row Y, every BAN row not triggered.**

| ID  | Cat  | Check                                                                                  | How to verify                                                                  |
| --- | ---- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| A1  | COMP | Motivation present (importance / pressure / impact, concrete)                          | Quote the sentence                                                             |
| A2  | COMP | Problem stated with scope                                                              | Quote the sentence                                                             |
| A3  | COMP | Approach named (system / method + mechanism)                                           | Quote the sentence                                                             |
| A4  | COMP | ≥ 1 quantitative result with named baseline                                            | Quote the number and the baseline name                                         |
| A5  | COMP | Implication / conclusion stated with scope                                             | Quote the sentence                                                             |
| A6  | DISC | Word count within venue cap                                                            | Report the exact integer word count                                            |
| A7  | DISC | Distinct numeric values in [1, 3]                                                      | List every number found                                                        |
| A8  | DISC | No figures, tables, citation markers, forward references                               | Scan for `[`, `Figure`, `Table`, `§`, `Section`, `Fig.`                        |
| A9  | DISC | All acronyms expanded on first use                                                     | List unexpanded acronyms                                                       |
| A10 | DISC | One continuous paragraph; no labels, no bullets                                        | Confirm absence of `\paragraph`, `-`, `*` at line start                        |
| A11 | DISC | Achievement verbs only                                                                 | List any effort verbs found                                                    |
| A12 | DISC | Title / abstract / §1 contributions name the same central concept                      | Quote all three                                                                |
| A13 | DISC | Single underline-able thesis sentence exists                                           | Quote it                                                                       |
| A14 | BAN  | Distinct numeric values ≤ 3                                                            | If count > 3, triggered                                                        |
| A15 | BAN  | No vague magnitude words without numbers                                               | List any offenders                                                             |
| A16 | BAN  | No forward references or inline citations                                              | List any offenders                                                             |
| A17 | BAN  | No prose-table-of-contents phrasing                                                    | List any offenders                                                             |
| A18 | BAN  | One primary claim                                                                      | Identify it; if two, list both                                                 |
| A19 | BAN  | No labeled fragments inside the abstract                                               | Confirm no `\paragraph` or bold inline labels                                  |
| A20 | BAN  | No training/test split numbers, ablation breakdowns, per-cell stats                    | List any §5-grade statistics found in the abstract                             |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GA1 | GEST | A reviewer can paraphrase the central claim in one sentence after one read     |
| GA2 | GEST | The paragraph has authorial voice — at least one sentence shows a judgment, a tension, or a deliberate scope choice |

## 7. Reviewer YAML output

```yaml
section: abstract
word_count: <int>
numeric_values_found: [<list>]
pass: <bool>
comp:
  A1: { y: <bool>, evidence: "<quote>" }
  A2: { y: <bool>, evidence: "<quote>" }
  A3: { y: <bool>, evidence: "<quote>" }
  A4: { y: <bool>, evidence: "<quote>" }
  A5: { y: <bool>, evidence: "<quote>" }
disc:
  A6:  { y: <bool>, value: <int>, venue_cap: <int> }
  A7:  { y: <bool>, count: <int> }
  A8:  { y: <bool>, offenders: [] }
  A9:  { y: <bool>, unexpanded: [] }
  A10: { y: <bool>, labels_found: [] }
  A11: { y: <bool>, effort_verbs: [] }
  A12: { y: <bool>, central_concept: "<>" }
  A13: { y: <bool>, thesis_sentence: "<>" }
ban:
  A14: { triggered: <bool>, count: <int> }
  A15: { triggered: <bool>, offenders: [] }
  A16: { triggered: <bool>, offenders: [] }
  A17: { triggered: <bool>, offenders: [] }
  A18: { triggered: <bool>, claims: [] }
  A19: { triggered: <bool>, labels: [] }
  A20: { triggered: <bool>, eval_grade_stats: [] }
gestalt:
  GA1: { y: <bool>, paraphrase: "<>" }
  GA2: { y: <bool>, voice_instance: "<>" }
minimum_fix: |
  <one paragraph naming the specific edits that flip pass to true>
```
