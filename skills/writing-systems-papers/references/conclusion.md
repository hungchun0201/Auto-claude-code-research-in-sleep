# Conclusion — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

§7 locks in the reader's memory and bounds the claim. It returns to the question §1 opened, names the strongest answer in one sentence, states the boundary condition that prevents over-claiming, and connects the result to a broader implication. §7 does not recap the paper; it synthesizes it.

§7 is short. It does not introduce new evidence, new contributions, or new figures.

## 2. Required components

| ID  | Cat  | Component             | Content                                                                                                  |
| --- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------- |
| K1  | COMP | Question mirror       | One sentence that mirrors §1's opening question or problem statement.                                    |
| K2  | COMP | Strongest answer      | One sentence stating the main result that addresses the question.                                        |
| K3  | COMP | Limitation            | At least one explicit limitation, scope condition, or failure regime named in §7 itself (not only in §5.7). |
| K4  | COMP | Implication           | One sentence stating what the result implies for design, practice, or future research, and the implication follows from the evidence. |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| K5  | DISC | Length: 120–300 words, up to 0.5 page if integrating discussion of limitations and broader implications.       |
| K6  | DISC | No new figures, tables, or numbers. The headline number, if mentioned, is the same as the abstract's headline number, verbatim. |
| K7  | DISC | No new claims, new contributions, or new mechanisms. Everything synthesized in §7 was supported earlier.       |
| K8  | DISC | The final sentence adds value: a crisp implication, a precise open question. Not a cliché ("we hope this paper inspires future work"). |
| K9  | DISC | The conclusion's central concept name matches the abstract, §1, §3, §5.                                       |
| K10 | DISC | Future work, if mentioned, is one or two concrete next questions. Not a list of broad ambitions.              |
| K11 | DISC | §7 paraphrases the abstract, it does not copy it. Word overlap with the abstract paragraph is below 30%.       |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| K12 | BAN | The conclusion is a near-verbatim restatement of the abstract (≥ 50% word overlap with the abstract paragraph, measured as fraction of shared content words). |
| K13 | BAN | A new claim, new contribution, new mechanism, or new experiment first appears in §7.                        |
| K14 | BAN | A future-work list with ≥ 4 broad ambitions and no concrete next question.                                  |
| K15 | BAN | A universal claim ("works in all settings", "fundamentally solves") not supported by the evidence in §5.    |
| K16 | BAN | No limitation stated at all in §7.                                                                          |
| K17 | BAN | A new number that does not appear elsewhere in the paper.                                                   |

## 5. Worked exemplar (Soar, MobiCom 2024)

Soar's §7 mirrors §1's question — *can smart roadside infrastructure deliver useful autonomous-driving support within a realistic power and cost budget?* — and answers it precisely: an 18-node deployment, supporting multiple autonomous-driving applications, within a power envelope that fits existing lamppost infrastructure.

The paragraph names one limitation in §7 itself: the deployment is at one site under one workload mix, and the support for higher-throughput perception models is not yet established. It then connects the result to a broader implication: smart roadside infrastructure is a viable layer in the autonomous-driving stack, complementing on-vehicle compute rather than replacing it.

The paragraph is roughly 220 words. It introduces no new figures and no new numbers. The closing sentence names a precise open question — extending the same deployment pattern to a multi-site network — rather than a list of generic future directions.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| K1  | COMP | One sentence mirrors §1 opening                                                             | Quote §1 opening and §7 mirror sentence                                        |
| K2  | COMP | Strongest answer stated in one sentence                                                     | Quote the sentence                                                             |
| K3  | COMP | At least one limitation stated in §7 itself                                                 | Quote the limitation                                                           |
| K4  | COMP | Implication present, supported by evidence                                                  | Quote implication; identify supporting evidence                                |
| K5  | DISC | Word count in [120, 300]                                                                    | Report actual count                                                            |
| K6  | DISC | No new figures, tables, or new numbers                                                      | List any new numbers                                                           |
| K7  | DISC | No new claims, contributions, or mechanisms                                                 | List any new content                                                           |
| K8  | DISC | Final sentence adds value                                                                   | Quote final sentence                                                           |
| K9  | DISC | Central concept name consistent with abstract / §1 / §3 / §5                                | Quote name in each location                                                    |
| K10 | DISC | Future work, if present, is ≤ 2 concrete next questions                                     | List future-work items                                                         |
| K11 | DISC | Word overlap with abstract < 30%                                                            | Compute overlap percentage                                                     |
| K12 | BAN  | No near-verbatim restatement of abstract (overlap < 50%)                                    | Compute overlap; flag if ≥ 50%                                                 |
| K13 | BAN  | No new claim / contribution / mechanism / experiment in §7                                  | List any                                                                       |
| K14 | BAN  | No future-work laundry list                                                                 | Count future-work items                                                        |
| K15 | BAN  | No unsupported universal claim                                                              | List flagged claims                                                            |
| K16 | BAN  | §7 contains a limitation                                                                    | Confirm presence                                                               |
| K17 | BAN  | No new number that does not appear elsewhere                                                | List any new numbers                                                           |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GK1 | GEST | §7 says something not already said in the abstract — a synthesis, a scope statement, a broader implication |
| GK2 | GEST | §7 has authorial voice — a deliberate concession, a precise scope choice, or a sharp open question |

## 7. Reviewer YAML output

```yaml
section: conclusion
word_count: <int>
abstract_overlap_pct: <float>
pass: <bool>
comp:
  K1: { y: <bool>, intro_opening: "<>", conclusion_mirror: "<>" }
  K2: { y: <bool>, answer_sentence: "<>" }
  K3: { y: <bool>, limitation: "<>" }
  K4: { y: <bool>, implication: "<>", supporting_evidence: "<>" }
disc:
  K5:  { y: <bool>, value: <int> }
  K6:  { y: <bool>, new_numbers: [] }
  K7:  { y: <bool>, new_content: [] }
  K8:  { y: <bool>, final_sentence: "<>" }
  K9:  { y: <bool>, central_concept: "<>" }
  K10: { y: <bool>, future_work_items: [] }
  K11: { y: <bool>, overlap: <float> }
ban:
  K12: { triggered: <bool>, overlap: <float> }
  K13: { triggered: <bool>, new_content: [] }
  K14: { triggered: <bool>, count: <int> }
  K15: { triggered: <bool>, claims: [] }
  K16: { triggered: <bool> }
  K17: { triggered: <bool>, new_numbers: [] }
gestalt:
  GK1: { y: <bool>, synthesis: "<>" }
  GK2: { y: <bool>, voice_instance: "<>" }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
