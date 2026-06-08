# Introduction — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

The introduction converts an area-level problem into *this* paper's falsifiable claim. It orients a broad reader, satisfies a skeptical reviewer, and seeds the contributions §1 promises later sections will deliver. A reviewer reading only §1 must be able to answer: is this important, is it hard, and does the paper plausibly solve it.

The introduction is continuous prose organized in paragraphs. Section roles (stakes, gap, idea, contributions) are performed by topic sentences. They are never announced by inline labels.

## 2. Required components

| ID  | Cat  | Component       | Content                                                                                                  |
| --- | ---- | --------------- | -------------------------------------------------------------------------------------------------------- |
| I1  | COMP | Stakes          | One paragraph naming the broader pressure: deployment scale, cost, workload growth, missed opportunity. Concrete numbers or named deployments. |
| I2  | COMP | Gap             | A single sentence that names what existing approaches miss, leave on the table, or trade off poorly. The reader can highlight one sentence. |
| I3  | COMP | Hard            | A paragraph or topic sentence explaining why obvious or incremental fixes do not close the gap.          |
| I4  | COMP | Idea preview    | One sentence stating the paper's design idea in shape, before any mechanism detail.                      |
| I5  | COMP | Contributions   | 3–5 numbered items. Each is specific, distinct, testable, outcome-shaped, and points to the section that proves it. |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| I6  | DISC | Open wide, narrow gradually. Paragraph 1 must not lead with API / kernel / hardware / code-path detail.       |
| I7  | DISC | The gap sentence (I2) appears in the first half of §1 and is a single sentence — not split across paragraphs. |
| I8  | DISC | The idea preview (I4) appears before any concrete mechanism description.                                      |
| I9  | DISC | Contributions read as outcomes: "We show that X reduces Y by Z." Not "We propose a method and evaluate it."   |
| I10 | DISC | Each contribution names the section that delivers it ("…(§5.2)"), not the figure or table number.             |
| I11 | DISC | Contributions do not carry training/test split percentages, held-out validation numbers, or per-cell statistics. Those belong in §5. |
| I12 | DISC | Length: 700–1100 words for a 10-page MLSys paper; 900–1400 words for a 12-page paper. Before figures.         |
| I13 | DISC | At most one figure in §1. If present, it must be readable in under 15 seconds and convey either the motivating bottleneck or the one-box system overview. |
| I14 | DISC | No inline rhetorical-role labels: do not write `\paragraph{The problem}`, `\paragraph{The gap}`, `\paragraph{The thesis}`, `\paragraph{Contributions}`, `\paragraph{Roadmap}`, or bold equivalents. Topic sentences perform the role. |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| I15 | BAN | Inline rhetorical-role labels anywhere in §1.                                                               |
| I16 | BAN | A contribution bullet stating training/test split percentages, ablation breakdowns, or held-out validation numbers. |
| I17 | BAN | Flat laundry-list contributions: ≥ 6 bullets, or bullets with no identifiable central claim.                |
| I18 | BAN | Literature dump: ≥ 10 citations in §1 with fewer than half contrasted on a named axis.                      |
| I19 | BAN | Chronological project narrative: "First we tried X, then Y, then Z".                                        |
| I20 | BAN | The gap (I2) is split across more than two paragraphs and cannot be quoted as a single sentence.            |
| I21 | BAN | A contribution claim whose target section does not actually deliver it (orphan contribution).               |
| I22 | BAN | "We describe / discuss / present and evaluate …" prose-table-of-contents phrasing.                          |

## 5. Worked exemplar (eRPC, NSDI 2019)

eRPC's §1 opens with the field's standing debate: *can a general-purpose RPC library match specialized systems?* That sentence is the entire introduction's hook. The paragraphs that follow execute the standard pattern, but every role is performed by a topic sentence, not announced.

1. **Stakes paragraph** — datacenter RPCs run everywhere; performance bottlenecks them; specialized systems exist but lock callers into one transport or NIC family.
2. **Gap sentence** — one sentence: general-purpose RPC libraries trail specialized systems at low microsecond latency.
3. **Hard paragraph** — kernel bypass alone is insufficient; batching alone is insufficient; polling alone is insufficient; the question is whether the right combination of small choices, together, can close the gap.
4. **Idea preview** — one sentence: a carefully composed set of design choices does close the gap, and the paper identifies which choices and why.
5. **Contributions** — three numbered outcomes, each ending with a section pointer.

§1 of eRPC carries no `\paragraph{The gap}` label. The gap is named in the third paragraph's topic sentence. The reader who skims will still find the gap because the topic sentence carries the rhetorical weight.

When drafting your own §1, write topic sentences that perform each role. Do not name the role.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| I1  | COMP | Stakes paragraph present with concrete numbers or named deployments                         | Quote the paragraph topic sentence                                             |
| I2  | COMP | Gap is a single underline-able sentence                                                     | Quote the sentence                                                             |
| I3  | COMP | Hard paragraph present, explaining why obvious fixes fail                                   | Quote the topic sentence                                                       |
| I4  | COMP | Idea preview present in one sentence, before mechanism detail                               | Quote the sentence                                                             |
| I5  | COMP | 3–5 numbered contributions, each outcome-shaped and section-anchored                        | Quote each contribution; confirm section pointers                              |
| I6  | DISC | Paragraph 1 does not lead with API / kernel / hardware / code detail                        | Quote paragraph 1 opening                                                      |
| I7  | DISC | Gap sentence is in the first half of §1 and is a single sentence                            | Report position; confirm singleness                                            |
| I8  | DISC | Idea preview precedes any mechanism description                                             | Confirm order                                                                  |
| I9  | DISC | Contributions are outcome-shaped, not activity-shaped                                       | Classify each bullet "outcome" vs "activity"                                   |
| I10 | DISC | Each contribution names a section that delivers it                                          | List (contribution, section pointer) pairs                                     |
| I11 | DISC | No training/test split numbers, held-out percentages, or per-cell stats in contributions    | List any §5-grade numbers found                                                |
| I12 | DISC | Length within range (700–1100 for 10pg; 900–1400 for 12pg, before figures)                  | Report actual word count                                                       |
| I13 | DISC | ≤ 1 figure; if present, readable in < 15s and one-purpose                                   | Describe the figure's single purpose                                           |
| I14 | DISC | No inline rhetorical-role labels                                                            | Grep for `\paragraph{The`, `\paragraph{Contribution`, `\textbf{The problem`    |
| I15 | BAN  | No inline rhetorical-role labels in §1                                                      | If any match found, triggered                                                  |
| I16 | BAN  | No §5-grade statistics inside any contribution bullet                                       | List offenders                                                                 |
| I17 | BAN  | Not a flat laundry list: ≤ 5 contributions and a central one identifiable                   | Count bullets, identify central                                                |
| I18 | BAN  | Not a literature dump                                                                       | Count §1 citations; classify each "contrasted" vs "name-dropped"               |
| I19 | BAN  | No chronological project narrative                                                          | Quote offending passage if present                                             |
| I20 | BAN  | Gap is one sentence                                                                         | Confirm singleness                                                             |
| I21 | BAN  | No orphan contribution                                                                      | For each contribution, verify its target section delivers it                   |
| I22 | BAN  | No prose-table-of-contents phrasing                                                         | Quote offenders                                                                |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GI1 | GEST | A reader who reads only §1 can predict, with > 50% accuracy, what §3 will look like |
| GI2 | GEST | §1 has authorial voice — a judgment, a tension, or a concession the reader recognizes |

## 7. Reviewer YAML output

```yaml
section: introduction
word_count: <int>
figure_count: <int>
pass: <bool>
comp:
  I1: { y: <bool>, evidence: "<quote>" }
  I2: { y: <bool>, gap_sentence: "<quote>" }
  I3: { y: <bool>, evidence: "<quote>" }
  I4: { y: <bool>, idea_sentence: "<quote>" }
  I5: { y: <bool>, contributions: [{ text: "<>", section: "<>" }] }
disc:
  I6:  { y: <bool>, opening: "<>" }
  I7:  { y: <bool>, position: "<paragraph N of M>" }
  I8:  { y: <bool> }
  I9:  { y: <bool>, classification: [] }
  I10: { y: <bool>, pairs: [] }
  I11: { y: <bool>, eval_grade_numbers_found: [] }
  I12: { y: <bool>, value: <int> }
  I13: { y: <bool>, count: <int> }
  I14: { y: <bool>, labels_found: [] }
ban:
  I15: { triggered: <bool>, labels: [] }
  I16: { triggered: <bool>, offenders: [] }
  I17: { triggered: <bool>, count: <int>, central: "<>" }
  I18: { triggered: <bool>, citation_count: <int>, contrasted: <int> }
  I19: { triggered: <bool>, quote: "<>" }
  I20: { triggered: <bool> }
  I21: { triggered: <bool>, orphans: [] }
  I22: { triggered: <bool>, offenders: [] }
gestalt:
  GI1: { y: <bool>, predicted_mechanism: "<>" }
  GI2: { y: <bool>, voice_instance: "<>" }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
