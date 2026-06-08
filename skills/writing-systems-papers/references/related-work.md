# Related Work — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

Related work makes the paper's novelty legible and fair. It clusters the field by approach or design point, contrasts nearest neighbors on named axes, and positions the paper against the prior work a reviewer is most likely to invoke as a reason to reject. Vague familiarity-signaling — listing citations to demonstrate the authors have read — is the opposite of what §6 is for.

## 2. Required components

| ID  | Cat  | Component             | Content                                                                                                  |
| --- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------- |
| W1  | COMP | Novelty sentence      | One sentence stating the paper's delta over the closest prior work, naming both.                          |
| W2  | COMP | Clusters              | The literature is grouped into ≥ 2 named clusters by approach / goal / deployment setting / hardware assumption. Each cluster is a paragraph or a small set of paragraphs. |
| W3  | COMP | Nearest-neighbor contrast | The papers a reviewer is most likely to ask about receive the most space. Each is contrasted on a named axis. |
| W4  | COMP | Charitable summaries  | Every cited paper has a fair, technically precise one-sentence summary of what it actually does.         |
| W5  | COMP | Complete references   | Every citation resolves via DBLP, CrossRef, the venue's proceedings page, or a stable preprint URL.       |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| W6  | DISC | Each cluster paragraph contains at least one explicit contrast on a named axis (e.g., generality vs latency, hardware assumption, decomposability, fit-free vs learned). |
| W7  | DISC | Length: 0.5–1.0 page in tight 12-page venues / MLSys; up to 1.25 pages in especially crowded SIGCOMM / MobiCom topics. |
| W8  | DISC | Comparison tables are permitted only when they compress methodology axes — not accuracy / latency / throughput numbers drawn from different workloads. If the column is a measured number, the table must use a single workload across all rows or be split into separate same-workload tables. |
| W9  | DISC | "First to X" claims are narrow, testable, and verified against the literature. Broad "first ever" framing is replaced with a precise scope ("first to evaluate one closed-form predictor on four NVIDIA SKUs"). |
| W10 | DISC | Citations are organized by cluster, not chronologically. Avoid the "In 2018 … In 2020 … In 2023 …" pattern.   |
| W11 | DISC | Verify every BibTeX entry before submission via DBLP → CrossRef → DOI. Never generate a citation from memory. |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| W12 | BAN | Comparison table where the column is a measured number and the rows draw those numbers from different workloads. (Universal U3; flagged in evaluation E17 as well.) |
| W13 | BAN | Laundry-list paragraph: one long sentence with ≥ 6 bracketed citations and no contrast.                     |
| W14 | BAN | "First to do X" claim that is not narrowed, scoped, and verified against the literature.                    |
| W15 | BAN | Chronological organization with year-based topic sentences.                                                 |
| W16 | BAN | A nearest neighbor (a paper that does almost the same thing) is omitted entirely.                            |
| W17 | BAN | A fabricated, hallucinated, or unverifiable BibTeX entry. (Universal U4.)                                   |
| W18 | BAN | Strawman summary of prior work: oversimplified, technically inaccurate, or attacking what a paper does not actually claim. |

## 5. Worked exemplar (eRPC, NSDI 2019)

eRPC's §6 does not pretend the paper appeared from nowhere. The section opens by situating eRPC in the RPC lineage: it names the family of specialized systems (FaSST, Erpc-predecessors, RDMA-based RPC frameworks) and the family of general-purpose RPC libraries (gRPC, Thrift, Apache Avro). Each family becomes a cluster paragraph.

The nearest neighbors — FaSST and gRPC — receive the most space. The FaSST paragraph names the technique FaSST uses, the result FaSST achieves, the workload class FaSST targets, and the axis on which eRPC differs (generality without losing the FaSST-class performance). The gRPC paragraph performs the symmetric contrast.

§6 contains no accuracy table comparing eRPC and FaSST on different workloads. When the paper wants to position itself against FaSST quantitatively, it does so in §5 with FaSST re-run on the eRPC workload, or it limits §6's claims to qualitative methodology axes.

The phrase "first ever" does not appear. The closest precise claim — that eRPC is the first general-purpose RPC library to match specialized-system performance on a specific class of datacenter workloads — is scoped, defensible, and verified against the literature.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| W1  | COMP | Single-sentence novelty claim names closest prior work                                      | Quote the sentence                                                             |
| W2  | COMP | ≥ 2 named clusters                                                                          | List cluster labels                                                            |
| W3  | COMP | Nearest neighbors receive most space, contrasted on named axes                              | Identify nearest neighbors; report space allocation; list axes                 |
| W4  | COMP | Every cited paper has a charitable, technically precise summary                             | Spot-check 5 citations; classify each "charitable" vs "strawman"               |
| W5  | COMP | Every BibTeX entry verifiable                                                               | Spot-check 5 entries against DBLP / CrossRef / DOI                             |
| W6  | DISC | Each cluster paragraph contains ≥ 1 explicit contrast on a named axis                       | Quote contrast sentence per cluster                                            |
| W7  | DISC | Length within [0.5, 1.0] page or up to 1.25 for crowded topics                              | Report page count                                                              |
| W8  | DISC | No comparison table mixing workloads in measured-number columns                             | Inspect every table; verify single-workload rule                               |
| W9  | DISC | "First to X" claims scoped and verified                                                     | Quote each "first" claim and its scope                                         |
| W10 | DISC | Organization by cluster, not by year                                                        | Inspect cluster topic sentences                                                |
| W11 | DISC | Every citation verified via DBLP / CrossRef / DOI                                           | Confirm                                                                        |
| W12 | BAN  | No apples-to-oranges accuracy table                                                         | List any offenders                                                             |
| W13 | BAN  | No laundry-list citation paragraph                                                          | Quote offending paragraphs                                                     |
| W14 | BAN  | No unverified "first" claim                                                                 | List offenders                                                                 |
| W15 | BAN  | No chronological organization                                                               | Quote any year-based topic sentence                                            |
| W16 | BAN  | No nearest-neighbor omission                                                                | Confirm coverage of expected nearest neighbors                                 |
| W17 | BAN  | No fabricated citations                                                                     | List unverifiable entries                                                      |
| W18 | BAN  | No strawman summaries                                                                       | List flagged summaries                                                         |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GW1 | GEST | A reviewer who has read §6 can name the paper's novelty in one sentence        |
| GW2 | GEST | §6 reads as positioning prose, not as citation-density signaling               |

## 7. Reviewer YAML output

```yaml
section: related_work
page_count: <float>
cluster_count: <int>
citation_count: <int>
pass: <bool>
comp:
  W1: { y: <bool>, novelty_sentence: "<>" }
  W2: { y: <bool>, clusters: [{ label: "<>", papers: <int> }] }
  W3: { y: <bool>, nearest_neighbors: [{ paper: "<>", axis: "<>" }] }
  W4: { y: <bool>, summary_classification: [] }
  W5: { y: <bool>, unverifiable: [] }
disc:
  W6:  { y: <bool>, contrast_sentences: [] }
  W7:  { y: <bool>, value: <float> }
  W8:  { y: <bool>, tables_inspected: [] }
  W9:  { y: <bool>, first_claims: [] }
  W10: { y: <bool> }
  W11: { y: <bool> }
ban:
  W12: { triggered: <bool>, offenders: [] }
  W13: { triggered: <bool>, quotes: [] }
  W14: { triggered: <bool>, claims: [] }
  W15: { triggered: <bool>, quote: "<>" }
  W16: { triggered: <bool>, omitted: [] }
  W17: { triggered: <bool>, entries: [] }
  W18: { triggered: <bool>, summaries: [] }
gestalt:
  GW1: { y: <bool>, novelty_paraphrase: "<>" }
  GW2: { y: <bool> }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
