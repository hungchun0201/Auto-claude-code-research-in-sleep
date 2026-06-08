# Design — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

§3 makes the central technical choices look inevitable. The goal is not to enumerate mechanism detail; it is to show that the choices made are principled given the requirements from §2, that the design is implementable, and that the dominant alternative was considered and rejected for a named reason.

§3 is continuous prose organized around a small number of mechanisms. Each mechanism is a subsection. The subsection's rationale — why this mechanism, what it does, what it costs — is woven into prose. A recurring four-block template (`Why / What / Tradeoff / Named alternative`) repeated across every mechanism reads as a checklist and is banned.

## 2. Required components

| ID  | Cat  | Component             | Content                                                                                                  |
| --- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------- |
| D1  | COMP | Goals and non-goals   | A subsection or paragraph stating the design's optimization targets and the explicit non-goals.          |
| D2  | COMP | Architecture overview | An overview figure and a topic-sentence summary of the architecture, placed before mechanism detail.     |
| D3  | COMP | Mechanism subsections | One subsection per named mechanism. Each subsection establishes the mechanism's challenge, the chosen approach, and the cost of the choice — through prose, not through a labeled four-block template. |
| D4  | COMP | Alternatives          | For every major design choice, name the dominant alternative the reader would expect, and explain in prose why it was not chosen. |
| D5  | COMP | Assumptions           | State the workload / hardware / trust / failure-model assumptions.                                       |
| D6  | COMP | Requirement coverage  | Build a (R_i → mechanism) map: every motivation requirement R_i is addressed by at least one mechanism.  |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| D7  | DISC | Architecture overview figure appears before mechanism depth, not after.                                       |
| D8  | DISC | Mechanism subsections do not share a recurring four-block label template. Specifically: do not place `\paragraph{Why}`, `\paragraph{What}`, `\paragraph{Tradeoff}`, `\paragraph{Named alternative}` (or bold inline equivalents) at the start of more than one mechanism subsection. Each subsection's rationale must be woven into prose. |
| D9  | DISC | Mechanism order is problem-driven, not chronological. Do not write "First we tried X, then we refactored to Y." |
| D10 | DISC | Implementation details (LOC, library version, code path) belong to §4, not §3.                                |
| D11 | DISC | Length: 2.5–4.0 pages for a 10-page MLSys paper; 3.0–5.0 pages for a 12-page paper.                           |
| D12 | DISC | 2–5 figures in §3. Each figure has an informative caption (states the conclusion the reader should draw). Figures are legible in grayscale at print size. |
| D13 | DISC | Each major design choice discusses its alternative in the same paragraph or adjacent paragraph, not in a recurring labeled block. |
| D14 | DISC | The design's central concept name appears in §3.1 (or §3.2 if §3.1 is goals-and-non-goals) and is consistent with the name used in the abstract and §1 contributions. |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| D15 | BAN | Recurring four-block label template (`Why / What / Tradeoff / Named alternative`, or `Goal / Mechanism / Cost / Alternative`, etc.) appearing as inline labels in 3+ mechanism subsections. |
| D16 | BAN | A mechanism subsection with no named alternative.                                                            |
| D17 | BAN | A mechanism subsection that exists with no corresponding R_i from §2 (orphan mechanism).                    |
| D18 | BAN | An R_i from §2 with no mechanism that addresses it (orphan requirement).                                    |
| D19 | BAN | Implementation-level details (LOC counts, library versions, code paths) inside a §3 mechanism description. |
| D20 | BAN | Chronological project narrative: "First we implemented X, then we refactored to Y."                         |
| D21 | BAN | Bag-of-tricks structure: ≥ 6 micro-optimizations listed without a unifying design principle.                |

## 5. Worked exemplar (Homa, SIGCOMM 2018)

Homa's §3 opens with a one-paragraph overview that names the controlling idea: an unscheduled portion plus a scheduled portion, with receiver-driven grants and dynamic priorities. The overview is followed by a single architecture figure. Then each mechanism becomes a subsection.

The unscheduled-portion subsection reads as prose. It begins with the design pressure (short messages should not pay scheduling latency), then names the mechanism (a small unscheduled prefix), then admits the cost (a few unscheduled packets may collide). The named alternative (always scheduling, as TIMELY does) is named in the third paragraph of the same subsection, with a one-sentence reason for rejection.

No subsection has `\paragraph{Why}` / `\paragraph{What}` / `\paragraph{Tradeoff}` labels. The rationale is in the topic sentences. The reader who skims the first sentence of each paragraph still gets the mechanism's purpose, mechanism, and cost.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| D1  | COMP | Goals and non-goals stated                                                                  | Quote both                                                                     |
| D2  | COMP | Architecture overview figure exists and is placed before mechanism detail                   | Identify figure; report position                                               |
| D3  | COMP | One subsection per named mechanism                                                          | List subsections                                                               |
| D4  | COMP | Each major design choice names the dominant alternative                                     | For each mechanism, identify (choice, alternative, reason for rejection)       |
| D5  | COMP | Assumptions stated                                                                          | Quote assumptions                                                              |
| D6  | COMP | (R_i → mechanism) map complete: every R_i has at least one mechanism                        | Provide the map                                                                |
| D7  | DISC | Overview figure precedes mechanism depth                                                    | Confirm order                                                                  |
| D8  | DISC | No recurring four-block label template across mechanisms                                    | Count subsections that share label scaffolding; must be ≤ 1                    |
| D9  | DISC | Mechanism order is problem-driven, not chronological                                        | Inspect subsection titles and topic sentences                                  |
| D10 | DISC | No implementation-level detail in §3                                                        | List any LOC counts / library versions / code paths found                      |
| D11 | DISC | Length in [2.5, 4.0] pages (10pg) or [3.0, 5.0] pages (12pg)                                | Report page count                                                              |
| D12 | DISC | 2–5 figures, each with informative caption, grayscale-legible                               | Count figures; classify captions "informative" vs "nominal"                    |
| D13 | DISC | Alternatives are woven into prose adjacent to the choice                                    | Spot-check                                                                     |
| D14 | DISC | Central concept name consistent across abstract / §1 / §3                                   | Quote each instance                                                            |
| D15 | BAN  | No recurring four-block label template in 3+ subsections                                    | Count subsections with `\paragraph{Why}` etc.                                  |
| D16 | BAN  | Every mechanism subsection names an alternative                                             | List subsections missing one                                                   |
| D17 | BAN  | No orphan mechanism                                                                         | List orphans                                                                   |
| D18 | BAN  | No orphan requirement                                                                       | List orphans                                                                   |
| D19 | BAN  | No implementation-level details in §3                                                       | List offenders                                                                 |
| D20 | BAN  | No chronological project narrative                                                          | Quote offenders                                                                |
| D21 | BAN  | Mechanism count is not bag-of-tricks (≤ 5 named mechanisms unified by a stated principle)   | List mechanisms and the unifying principle                                     |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GD1 | GEST | A reviewer can reconstruct the architecture in their own words after one read of §3 |
| GD2 | GEST | §3 reads as prose, not as a recurring template. Subsections do not share the same template scaffolding |
| GD3 | GEST | §3 has authorial voice — at least one sentence shows the author's judgment about the difficulty of the choice |

## 7. Reviewer YAML output

```yaml
section: design
page_count: <float>
mechanism_count: <int>
figure_count: <int>
pass: <bool>
comp:
  D1: { y: <bool>, goals: [], non_goals: [] }
  D2: { y: <bool>, figure_id: "<>", position: "<>" }
  D3: { y: <bool>, mechanisms: [] }
  D4: { y: <bool>, choices: [{ choice: "<>", alternative: "<>", reason: "<>" }] }
  D5: { y: <bool>, assumptions: [] }
  D6: { y: <bool>, map: { R1: ["§3.x"], R2: ["§3.y"] } }
disc:
  D7:  { y: <bool> }
  D8:  { y: <bool>, template_subsection_count: <int> }
  D9:  { y: <bool> }
  D10: { y: <bool>, offenders: [] }
  D11: { y: <bool>, value: <float> }
  D12: { y: <bool>, count: <int>, caption_classification: [] }
  D13: { y: <bool> }
  D14: { y: <bool>, central_concept: "<>" }
ban:
  D15: { triggered: <bool>, template_subsections: [] }
  D16: { triggered: <bool>, missing_alternative: [] }
  D17: { triggered: <bool>, orphan_mechanisms: [] }
  D18: { triggered: <bool>, orphan_requirements: [] }
  D19: { triggered: <bool>, offenders: [] }
  D20: { triggered: <bool>, quote: "<>" }
  D21: { triggered: <bool>, mechanism_count: <int> }
gestalt:
  GD1: { y: <bool>, reconstruction: "<>" }
  GD2: { y: <bool> }
  GD3: { y: <bool>, voice_instance: "<>" }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
