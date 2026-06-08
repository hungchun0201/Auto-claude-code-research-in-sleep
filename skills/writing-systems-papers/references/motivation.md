# Motivation — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

Motivation earns the reader's permission to spend the rest of the paper. It proves the pain point, explains why obvious or prior approaches fail, and leaves behind design requirements that §3 must satisfy. The convincing motivations are mismatch stories: generality versus performance, latency versus utilization, deployment reality versus academic assumption, scale versus controllability.

Motivation is continuous prose. Observations and requirements may be enumerated, but the prose between enumerations carries the argument. Enumeration is a tool for clarity, not a substitute for argument.

## 2. Required components

| ID  | Cat  | Component        | Content                                                                                                  |
| --- | ---- | ---------------- | -------------------------------------------------------------------------------------------------------- |
| M1  | COMP | Quantified pressure | At least one concrete number, workload fact, or deployment fact establishing the pain point.        |
| M2  | COMP | Named baseline insufficiency | Name the specific baseline a reasonable reviewer would propose and explain why it fails or trades off badly. |
| M3  | COMP | Design requirements | Convert the pressure and insufficiency into 2–4 design requirements (R1, R2, …). Each is testable.   |
| M4  | COMP | Assumptions       | Name the workload / hardware / trust / failure-model assumptions that make the motivation fair.         |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| M5  | DISC | Open with concrete pressure (a number, a workload, a deployment incident). Never with "X is becoming increasingly important." |
| M6  | DISC | Show insufficiency before stating the design requirement. The requirement is what the insufficiency *implies*. |
| M7  | DISC | The number of design requirements is in [2, 4]. Fewer is acceptable if the paper has only one mechanism; more is forbidden. |
| M8  | DISC | Each design requirement maps to a §3 mechanism that addresses it. Build the (R_i → mechanism) map before drafting §3. |
| M9  | DISC | Length: 250–600 words if motivation is a standalone subsection; otherwise it merges into §1.                  |
| M10 | DISC | ≤ 1 motivating figure. The figure makes the mismatch visible at a glance: a tradeoff frontier, a tail-latency curve, an application-mismatch histogram, a deployment diagram. |
| M11 | DISC | No mechanism details. The design idea may be hinted at the very end of §2 but its inner workings belong to §3. |
| M12 | DISC | No inline rhetorical-role labels. Do not write `\paragraph{Why this is hard}` or `\paragraph{Requirements}`. Topic sentences perform the role. |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| M13 | BAN | Generic-importance opener: "increasingly important", "growing demand", "ubiquitous", "essential in modern". |
| M14 | BAN | Future-fantasy motivation: more than one paragraph of speculative future scenarios with no current data.    |
| M15 | BAN | Mechanism details before the gap is settled.                                                                |
| M16 | BAN | Implicit or anonymous baseline: "no existing approach works" without naming at least one specific baseline. |
| M17 | BAN | Motivation built entirely on adjectives — no number, no workload, no deployment fact.                       |
| M18 | BAN | A design requirement R_i with no corresponding §3 mechanism.                                                |
| M19 | BAN | A §3 mechanism with no corresponding motivation requirement (orphan mechanism — flagged here, fails X2).    |

## 5. Worked exemplar (ChameleonAPI, OSDI 2024)

ChameleonAPI's motivation is convincing because it converts a vague complaint ("generic ML APIs are imperfect") into a measured systems problem.

1. **Pressure paragraph** — modern applications increasingly call hosted ML APIs rather than train their own models. The paper backs this with an empirical study of 77 real-world applications.
2. **Insufficiency paragraph** — different applications care about different output errors. A single generic API produces outputs that are correct on average but wrong for the specific application's decision.
3. **Requirements** — three design requirements: per-application output customization, low overhead, automatic without developer effort.
4. **Assumptions** — applications consume API outputs through small adapter code; the system has access to the application's decision logic.

No paragraph carries an inline label like `\paragraph{Requirements}`. The third paragraph ends with three requirements written into prose, then numbered for reference. The next section's mechanisms map onto these requirements one for one.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| M1  | COMP | Quantified pressure (number / workload / deployment fact)                                   | Quote the number and its source                                                |
| M2  | COMP | Named baseline insufficiency                                                                | Quote the baseline name and the failure reason                                 |
| M3  | COMP | 2–4 design requirements derived                                                             | List each requirement                                                          |
| M4  | COMP | Assumptions stated                                                                          | Quote the assumptions sentence                                                 |
| M5  | DISC | Concrete opener (no generic-importance phrasing)                                            | Quote opening sentence                                                         |
| M6  | DISC | Insufficiency precedes the requirement                                                      | Confirm order                                                                  |
| M7  | DISC | Requirement count in [2, 4]                                                                 | Report count                                                                   |
| M8  | DISC | Each R_i maps to a §3 mechanism                                                             | Build the (R_i → mechanism) map                                                |
| M9  | DISC | Length in [250, 600] words for standalone subsection                                        | Report word count                                                              |
| M10 | DISC | ≤ 1 motivating figure, single-purpose                                                       | Describe figure purpose                                                        |
| M11 | DISC | No mechanism details in §2                                                                  | Quote any premature mechanism description                                      |
| M12 | DISC | No inline rhetorical-role labels                                                            | Grep for `\paragraph{Why`, `\paragraph{Requirement`, `\textbf{Pressure`        |
| M13 | BAN  | No generic-importance opener                                                                | Quote offending opener if present                                              |
| M14 | BAN  | No future-fantasy paragraph                                                                 | Quote offending passage                                                        |
| M15 | BAN  | No premature mechanism details                                                              | Quote offenders                                                                |
| M16 | BAN  | Baseline is named, not anonymous                                                            | Quote baseline name                                                            |
| M17 | BAN  | Motivation contains at least one number or workload fact                                    | Confirm                                                                        |
| M18 | BAN  | No orphan R_i                                                                               | List orphans                                                                   |
| M19 | BAN  | No orphan §3 mechanism                                                                      | List orphans                                                                   |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GM1 | GEST | A reviewer can name the design requirements (R1–Rn) after one read of §2       |
| GM2 | GEST | §2 has authorial voice — at least one sentence shows judgment about why the tradeoff matters |

## 7. Reviewer YAML output

```yaml
section: motivation
word_count: <int>
requirement_count: <int>
pass: <bool>
comp:
  M1: { y: <bool>, evidence: "<quote>" }
  M2: { y: <bool>, baseline: "<>", failure_reason: "<>" }
  M3: { y: <bool>, requirements: [{ id: "R1", text: "<>" }, ...] }
  M4: { y: <bool>, evidence: "<quote>" }
disc:
  M5:  { y: <bool>, opener: "<>" }
  M6:  { y: <bool> }
  M7:  { y: <bool>, count: <int> }
  M8:  { y: <bool>, map: { R1: "§3.x", R2: "§3.y" } }
  M9:  { y: <bool>, value: <int> }
  M10: { y: <bool>, figure_purpose: "<>" }
  M11: { y: <bool>, premature_details: [] }
  M12: { y: <bool>, labels_found: [] }
ban:
  M13: { triggered: <bool>, opener: "<>" }
  M14: { triggered: <bool>, quote: "<>" }
  M15: { triggered: <bool>, offenders: [] }
  M16: { triggered: <bool> }
  M17: { triggered: <bool> }
  M18: { triggered: <bool>, orphans: [] }
  M19: { triggered: <bool>, orphans: [] }
gestalt:
  GM1: { y: <bool>, requirements_recalled: [] }
  GM2: { y: <bool>, voice_instance: "<>" }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
