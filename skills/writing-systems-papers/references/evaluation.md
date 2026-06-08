# Evaluation — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

§5 is a claim-verification engine, not a benchmark scrapbook. Every claim in the abstract, §1 contributions, or §3 design must have a named experiment in §5 that tests it. Every figure must support a specific conclusion stated in its caption. Stress, scale, sensitivity, and limitations are first-class content because they bound where the system can be deployed.

§5 also operates under the most enforced rule of systems-paper writing: *baselines are measured on the same workload as the proposed system*. Comparing your number against a baseline's paper-reported number on a different workload is not a comparison — it is a citation pretending to be evidence.

## 2. Required components

| ID  | Cat  | Component             | Content                                                                                                  |
| --- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------- |
| E1  | COMP | Evaluation questions  | The section opens with a short numbered list of the questions §5 will answer.                            |
| E2  | COMP | Claim → experiment map | Every contribution C_i in §1 and every design claim in §3 has a §5 experiment that tests it. The map is reconstructable. |
| E3  | COMP | Setup                 | Hardware, datasets / workloads, baselines (with tuning notes), default knobs, and number of runs / error reporting. |
| E4  | COMP | Fair baselines        | The strongest, most-tuned, currently published alternatives — measured on the same workload as the proposed system. |
| E5  | COMP | End-to-end first      | The first results subsection is the end-to-end comparison against baselines. Ablations come after.       |
| E6  | COMP | Ablations             | At least one ablation per major mechanism. Each ablation isolates the mechanism while holding everything else fixed. |
| E7  | COMP | Stress experiment     | At least one of: scaling, tail-latency under load, sensitivity to a key knob, robustness under workload shift. |
| E8  | COMP | Limitations           | A subsection naming where the system breaks or weakens, with the technical reason.                       |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| E9  | DISC | Each subsection opens with the question (or claim) it answers, then presents evidence, then states the conclusion. |
| E10 | DISC | Each figure caption states the conclusion the reader should draw, not the axis names. "Throughput vs batch size" is not a caption; "FlashInfer sustains throughput within 5% of the oracle scheduler across all batch sizes" is. |
| E11 | DISC | Hardware, batch size, dataset, and budget are matched across the proposed system and every baseline. Asymmetries are stated explicitly with their reason. |
| E12 | DISC | Stochastic experiments report error bars, variance, or number of runs.                                        |
| E13 | DISC | Length: 2.5–3.5 pages for 10pg MLSys; 3.0–4.5 pages for 12pg venues.                                          |
| E14 | DISC | 4–8 figures and tables combined. One setup table, two to four headline-result figures, one to two ablations, one stress / cost / robustness figure. |
| E15 | DISC | No inline rhetorical-role labels (`\paragraph{Setup}`, `\paragraph{Results}`, `\paragraph{Ablation}` are acceptable as subsection headers but not as inline labels inside a paragraph). |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| E16 | BAN | Any acceptance-critical claim supported only by an appendix figure / table at NSDI / MLSys / SIGCOMM / MobiCom. |
| E17 | BAN | A comparison table whose column is a measured number (accuracy, latency, throughput, MAPE, F1, etc.) and whose rows draw those numbers from different workloads / datasets / hardware. If the column is a measured number, all rows share one workload. Methodology axes (decomposable, fit-free, SKUs covered) are exempt. |
| E18 | BAN | "Apples-to-apples baseline runs are future work" or equivalent. If the paper does not have apples-to-apples baseline numbers, the claim cannot rest on a comparison-to-baseline statement. |
| E19 | BAN | Strawman baseline: an old, untuned, or known-inferior alternative used in place of the current state of the art. |
| E20 | BAN | Universal claim from a single workload, dataset, hardware configuration, or scale point.                    |
| E21 | BAN | A subsection of §5 with no leading question or claim.                                                       |
| E22 | BAN | Silent setup asymmetry between the proposed system and baselines (different batch size, hardware, dataset, budget) not disclosed in the setup subsection. |
| E23 | BAN | Headline results that depend on a baseline number copied from another paper's reported result on its own workload. |

## 5. Worked exemplar (ChameleonAPI, OSDI 2024)

ChameleonAPI's §5 opens with three explicit evaluation questions: how much the system reduces incorrect application decisions, how long customization takes, and whether the full method outperforms a simpler variant. The setup subsection names the 77 applications, the hardware, and the baselines, and reports the number of runs per measurement.

Each subsequent subsection begins with the question it answers. The headline result subsection compares the proposed system against the strongest currently available alternatives, on the same applications, with the same hardware, with the same input traces. The ablation subsection isolates the customization mechanism while holding the rest of the pipeline fixed. The limitations subsection names regimes where ChameleonAPI is less effective, with technical reasons.

The paper does not compare its accuracy against another system's paper-reported accuracy on a different workload. When the authors want to position their work against prior systems, they do so by re-running those systems on the 77 applications, or by restricting the comparison table to methodology axes.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| E1  | COMP | Evaluation questions stated at section opening                                              | Quote the question list                                                        |
| E2  | COMP | Claim → experiment map reconstructable                                                      | Build (claim → experiment) table; list any unsupported claim                   |
| E3  | COMP | Setup subsection enumerates hardware / datasets / baselines / knobs / runs                  | Quote each item                                                                |
| E4  | COMP | Baselines are strongest current alternatives, tuned                                         | Name baselines; confirm tuning details                                         |
| E5  | COMP | End-to-end comparison precedes ablations                                                    | Confirm section order                                                          |
| E6  | COMP | One ablation per major mechanism, isolating the mechanism                                   | List (mechanism, ablation) pairs                                               |
| E7  | COMP | At least one stress experiment                                                              | Identify subsection                                                            |
| E8  | COMP | Limitations subsection with technical reasons                                               | Quote limitations                                                              |
| E9  | DISC | Each subsection opens with its question                                                     | Quote each subsection's opening                                                |
| E10 | DISC | Captions are conclusion-bearing, not nominal                                                | Classify each caption                                                          |
| E11 | DISC | Setup matched across system and baselines; asymmetries disclosed                            | Confirm matching; list disclosed asymmetries                                   |
| E12 | DISC | Stochastic experiments report uncertainty                                                   | Quote the uncertainty reporting                                                |
| E13 | DISC | Length in [2.5, 3.5] (MLSys) or [3.0, 4.5] (12pg) pages                                     | Report page count                                                              |
| E14 | DISC | 4–8 figures and tables                                                                      | Report count                                                                   |
| E15 | DISC | No inline rhetorical-role labels inside paragraphs                                          | Grep for `\paragraph{` inside paragraph body                                   |
| E16 | BAN  | No appendix-only acceptance-critical claim                                                  | List any claim whose only evidence is in the appendix                          |
| E17 | BAN  | No apples-to-oranges accuracy table                                                         | List any comparison table flagged                                              |
| E18 | BAN  | No "apples-to-apples baselines are future work" disclaimer                                  | Quote any such disclaimer                                                      |
| E19 | BAN  | No strawman baseline                                                                        | List flagged baselines                                                         |
| E20 | BAN  | No universal claim from single workload / dataset / hardware                                | List universal claims; check evidence coverage                                 |
| E21 | BAN  | Every subsection has a leading question or claim                                            | List any subsection lacking one                                                |
| E22 | BAN  | No silent setup asymmetry                                                                   | List undisclosed asymmetries                                                   |
| E23 | BAN  | No headline result that depends on baseline numbers copied from another paper's workload    | List headline results; verify each baseline number is measured on this paper's workload |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GE1 | GEST | A reader can map every abstract claim to a §5 figure or table                  |
| GE2 | GEST | A reader who reads only figure captions and titles can summarize §5's conclusions accurately |
| GE3 | GEST | §5 acknowledges where the system weakens, in prose, with technical reasoning   |

## 7. Reviewer YAML output

```yaml
section: evaluation
page_count: <float>
figure_count: <int>
table_count: <int>
pass: <bool>
comp:
  E1: { y: <bool>, questions: [] }
  E2: { y: <bool>, claim_experiment_map: {} }
  E3: { y: <bool>, hardware: "<>", datasets: [], baselines: [], runs_per_cell: <int> }
  E4: { y: <bool>, baseline_tuning_notes: [] }
  E5: { y: <bool>, section_order: [] }
  E6: { y: <bool>, ablation_map: {} }
  E7: { y: <bool>, stress_subsection: "<>" }
  E8: { y: <bool>, limitations_quote: "<>" }
disc:
  E9:  { y: <bool>, subsection_openings: [] }
  E10: { y: <bool>, caption_classification: [] }
  E11: { y: <bool>, disclosed_asymmetries: [] }
  E12: { y: <bool>, uncertainty_reporting: "<>" }
  E13: { y: <bool>, value: <float> }
  E14: { y: <bool>, fig_count: <int>, table_count: <int> }
  E15: { y: <bool> }
ban:
  E16: { triggered: <bool>, appendix_only_claims: [] }
  E17: { triggered: <bool>, flagged_tables: [] }
  E18: { triggered: <bool>, disclaimer_quote: "<>" }
  E19: { triggered: <bool>, strawman_baselines: [] }
  E20: { triggered: <bool>, universal_claims: [] }
  E21: { triggered: <bool>, subsections_without_question: [] }
  E22: { triggered: <bool>, undisclosed_asymmetries: [] }
  E23: { triggered: <bool>, headline_results_with_copied_baselines: [] }
gestalt:
  GE1: { y: <bool>, abstract_to_figure_map: {} }
  GE2: { y: <bool>, caption_only_summary: "<>" }
  GE3: { y: <bool>, weakness_acknowledgment: "<>" }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
