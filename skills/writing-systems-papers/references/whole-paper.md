# Whole-Paper Reference

> Universal hard bans, paragraph discipline, cross-section consistency rubric, and gestalt rubric. Apply once per paper after all section-level rubrics have been scored.

## 1. Universal hard bans

Any single trigger forces round = FAIL regardless of per-section scores.

| ID  | Banned pattern                                                                                                  |
| --- | --------------------------------------------------------------------------------------------------------------- |
| U1  | Inline rhetorical-role labels in body text: `\paragraph{The problem}`, `\paragraph{The gap}`, `\paragraph{The thesis}`, `\paragraph{Contributions}`, `\paragraph{Roadmap}`, `\paragraph{Named alternative}`, `\paragraph{Why}`, `\paragraph{What}`, `\paragraph{Tradeoff}`. Section roles are paragraph functions and must be performed by topic sentences, not announced by headings. |
| U2  | More than two enumerated label series across the body. A series = a sequence sharing a label prefix (G1–Gn, O1–On, R1–Rn, M1–Mn, Q1–Qn, contributions 1–N). The paper may use at most two such series total. |
| U3  | Comparison tables whose columns are measured numbers (accuracy, latency, throughput, MAPE, F1, etc.) drawn from different workloads / datasets / hardware. If the column is numeric, all rows must come from the same workload. Comparison on methodology axes (decomposability, fit-free, SKUs covered) does not trigger this ban. |
| U4  | Fabricated, hallucinated, or unverifiable citations. Every reference must resolve via DBLP, CrossRef, the venue's proceedings page, or a stable preprint URL. |
| U5  | Any acceptance-critical claim that depends on appendix-only evidence at NSDI / MLSys / SIGCOMM / MobiCom. The main body must stand alone. |
| U6  | "We describe", "We discuss", "We present and evaluate", "In this paper we …" prose-table-of-contents phrasing in abstract, §1, or any contribution bullet. |
| U7  | Subsection-level "Why / What / Tradeoff / Named alternative" four-block templates appearing three or more times in §3. Mechanism rationale must be woven into prose, not announced. |
| U8  | The same statistic appearing in abstract, contributions, evaluation, and conclusion. A number belongs to its primary section. |
| U9  | File paths, filenames, function names, class names, struct names, JSON keys, configuration-knob names, CLI flag names, or shell commands in the body text of any section §1–§7. Components are named semantically in body prose. The appendix may include such identifiers when they are essential for reproducibility, capped at **≤ 8 distinct identifiers across the entire appendix**. The body of §1–§7 contains zero. (Matches `*.py`, `*.cpp`, `*.cu`, `*.json`, `*.h`, `*.sh`, `*.tex`, `*.yaml`, `*.toml`, function-call notation `foo()`, `Class::method`, `obj.field`, any path containing `/` other than inside `\url{}`.) |
| U10 | Any `Overfull \hbox` warning > 5pt in the compiled `main.log`. See `typography.md` for the verification procedure and the LaTeX patterns that cause overflow. |

## 2. Paragraph discipline (universal)

`\paragraph{...}` is a legitimate LaTeX tool. The discipline below governs *how* it is used, not whether. A `\paragraph{X}` label promises a developed paragraph about `X` — at least several sentences that establish, argue, and conclude one named idea. A 1- to 3-sentence paragraph under a `\paragraph{}` label is a *framework-question stub*: the label names a question imposed by an external rubric (Why, What, Tradeoff, Goal, …) and the paragraph supplies a one-liner answer. A subsection composed of three or more such stubs reads as a Q&A document, not as an argument.

The rules below distinguish two cases:

- **Permitted**: an occasional `\paragraph{X}` where `X` is a *content-specific entity* (a named mechanism, regime, phenomenon, or decision) and the paragraph develops it across ≥ 4 sentences. Examples that pass: `\paragraph{Bandwidth-bound regime.}`, `\paragraph{Receiver-driven priority assignment.}`, `\paragraph{Per-step latency under high load.}`
- **Banned**: a stack of `\paragraph{X_i}` blocks where each `X_i` names an abstract framework question and each block answers in 1–3 sentences. Examples that fail: `\paragraph{Why.}`, `\paragraph{What.}`, `\paragraph{Tradeoff.}`, `\paragraph{Named alternative.}`, `\paragraph{Goals.}`, `\paragraph{Setup.}`, `\paragraph{Approach.}`, `\paragraph{Rationale.}`

### 2.1 Hard bans (paragraph structure)

| ID  | Cat | Banned pattern                                                                                                |
| --- | --- | ------------------------------------------------------------------------------------------------------------- |
| P1  | BAN | A `\paragraph{...}`-led paragraph contains fewer than 4 sentences. A `\paragraph{}` label promises a developed paragraph; a labeled stub is a Q&A entry in disguise. |
| P2  | BAN | Two or more consecutive body paragraphs are each both `\paragraph{}`-led **and** fewer than 5 sentences. One short emphasized paragraph is permitted; consecutive short labeled paragraphs form a Q&A run. |
| P3  | BAN | A single subsection contains three or more `\paragraph{}`-led paragraphs where each is fewer than 5 sentences. This is the framework-question-stack pattern. |
| P4  | BAN | A `\paragraph{X}` label where `X` is an abstract framework term: any of `Why`, `What`, `How`, `Tradeoff`, `Tradeoffs`, `Goal`, `Goals`, `Non-goals`, `Approach`, `Method`, `Setup`, `Result`, `Results`, `Conclusion`, `Limitation`, `Limitations`, `Motivation`, `Discussion`, `Background`, `Overview`, `Architecture`, `Rationale`, `Named alternative`, `Alternative`, `Why this is hard`, `Why this works`, `The problem`, `The gap`, `The thesis`, `Contributions`, `Roadmap`. The legitimate `\paragraph{}` label names a content-specific entity in this paper, not a rubric question. |
| P5  | BAN | Mean body paragraph length across the paper is fewer than 5 sentences or fewer than 100 words. (Body = non-caption, non-list-item, non-equation prose.) |

### 2.2 Discipline (paragraph flow)

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| P6  | DISC | When `\paragraph{X}` is used, `X` names a content-specific entity that this paper introduces or develops (a mechanism, regime, phenomenon, design choice, observation). `X` is not a rubric question, not a generic section role, not a placeholder. |
| P7  | DISC | Consecutive paragraphs are connected: each paragraph after the first opens with a connective signal — a pronoun back-reference, an entity continuation, or a transition phrase (*However, This means, As a result, More specifically, But this requires, In contrast, The harder case, Conversely*). |
| P8  | DISC | Each paragraph's first sentence advances the argument from the previous paragraph. It is not a rephrased rubric question, not a section-template prompt, and not a label-in-disguise. |
| P9  | DISC | A "why / what / tradeoff" rhythm in a subsection is integrated into one or two flowing paragraphs, not split into three labeled blocks. |

## 3. Cross-section consistency (X-rubric)

Run after all section files have been scored. Each row Y/N; any X-N failure triggers FAIL.

| ID  | Cat   | Check                                                                                                        | Verify by                                                                              |
| --- | ----- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| X1  | XSEC  | Every motivation requirement R_i has at least one design mechanism that addresses it                          | Build the (R_i → mechanism) map; list any orphan R_i                                   |
| X2  | XSEC  | Every design mechanism is justified by at least one motivation requirement                                    | Build the (mechanism → R_i) map; list any orphan mechanism                             |
| X3  | XSEC  | Every introduction contribution C_i is delivered by a named later section, and the section actually delivers | Build the (C_i → section) map; for each, quote one sentence from the target section that proves the contribution |
| X4  | XSEC  | Every conclusion claim is supported by a section that precedes it; no new claim debuts in §7                  | List conclusion claims; mark provenance section for each; flag any orphan              |
| X5  | XSEC  | The paper's central concept name (system / mechanism / claim) appears verbatim in: abstract, §1 contributions, §3 design overview, §5 evaluation framing, §7 conclusion | Quote each instance; confirm same name                                                |
| X6  | XSEC  | Total enumerated label series across the body ≤ 2                                                            | List every series: G1–Gn, O1–On, R1–Rn, M1–Mn, Q1–Qn, contribution list. If count > 2, fail. |
| X7  | XSEC  | No statistic appears in more than two sections                                                               | List every numeric value with the sections it appears in; flag any value appearing in ≥ 3 sections |
| X8  | XSEC  | The headline result number in the abstract matches the headline result number in §5 and in §7 verbatim       | Quote all three                                                                        |
| X9  | XSEC  | Reading only the first sentence of every body paragraph produces a coherent summary of the paper's argument  | Build the topic-sentence chain; confirm it reads as a connected narrative ≤ 30 sentences |

## 4. Whole-paper gestalt

Subjective; apply with reviewer judgment. Mark each Y/N with a one-sentence justification.

| ID  | Cat   | Check                                                                                                        |
| --- | ----- | ------------------------------------------------------------------------------------------------------------ |
| GP1 | GEST  | A reader who reads only the abstract can paraphrase the central claim in one sentence without copying phrases verbatim |
| GP2 | GEST  | A reader who reads only §1 can predict, with > 50% accuracy, what §3 mechanism will look like               |
| GP3 | GEST  | Every body section opens with a topic sentence that performs the section's role; no section is announced by a rhetorical-role label |
| GP4 | GEST  | The paper has authorial voice in at least three places — a judgment, a tension, a deliberate concession, an admission of difficulty |
| GP5 | GEST  | The paper does not read as a checklist. Reading consecutive subsections does not produce the same template shape (Why / What / Tradeoff / Named alternative) repeatedly |
| GP6 | GEST  | The paper has at least one moment of intellectual surprise — a finding, an observation, or a design choice the reader did not anticipate from the title and abstract |
| GP7 | GEST  | Body paragraphs are continuous prose, not enumerated short answers. The paper reads as a chain of paragraphs, not as a stack of bullets-disguised-as-`\paragraph{}`. |
| GP8 | GEST  | The topic-sentence chain (first sentences of body paragraphs, read in order) is coherent on its own. A reader skimming only topic sentences can follow the paper's argument. |

## 5. YAML output (whole-paper)

After scoring all section files, the reviewer emits one whole-paper YAML block:

```yaml
section: whole_paper
body_paragraph_count: <int>
mean_paragraph_sentences: <float>
mean_paragraph_words: <float>
paragraph_density_per_300_words: <float>
universal_hard_bans:
  U1:  { triggered: <bool>, evidence: [<list of \paragraph{...} matches>] }
  U2:  { triggered: <bool>, series_found: [<list>] }
  U3:  { triggered: <bool>, tables_flagged: [<list>] }
  U4:  { triggered: <bool>, unverifiable_citations: [<list>] }
  U5:  { triggered: <bool>, appendix_dependent_claims: [<list>] }
  U6:  { triggered: <bool>, offenders: [<quotes>] }
  U7:  { triggered: <bool>, count: <int> }
  U8:  { triggered: <bool>, repeated_stats: [<list>] }
  U9:  { triggered: <bool>, body_identifiers: [{ section: "<>", identifier: "<>" }], appendix_identifier_count: <int> }
  U10: { triggered: <bool>, max_overfull_pt: <float>, count: <int> }
paragraph:
  P1: { triggered: <bool>, short_labeled_paragraphs: [{ section: "<>", label: "<>", sentence_count: <int> }] }
  P2: { triggered: <bool>, consecutive_short_labeled_runs: [{ section: "<>", labels: [], lengths: [] }] }
  P3: { triggered: <bool>, offending_subsections: [{ section: "<>", short_labeled_count: <int>, labels: [] }] }
  P4: { triggered: <bool>, abstract_labels_found: [{ section: "<>", label: "<>" }] }
  P5: { triggered: <bool>, mean_sentences: <float>, mean_words: <float> }
  P6: { y: <bool>, non_content_labels: [{ section: "<>", label: "<>" }] }
  P7: { y: <bool>, paragraphs_without_connective: [{ section: "<>", opening: "<>" }] }
  P8: { y: <bool>, framework_question_openings: [{ section: "<>", opening: "<>" }] }
  P9: { y: <bool>, three_block_subsections: [] }
xsec:
  X1: { y: <bool>, orphan_requirements: [] }
  X2: { y: <bool>, orphan_mechanisms: [] }
  X3: { y: <bool>, contribution_section_map: {} }
  X4: { y: <bool>, orphan_conclusion_claims: [] }
  X5: { y: <bool>, central_concept_name: "<>" }
  X6: { y: <bool>, series_count: <int>, series_list: [] }
  X7: { y: <bool>, over_repeated_stats: [] }
  X8: { y: <bool>, abstract_number: "<>", eval_number: "<>", conclusion_number: "<>" }
  X9: { y: <bool>, topic_sentence_chain_coherent: <bool>, chain_summary: "<>" }
gestalt:
  GP1: { y: <bool>, paraphrase: "<>" }
  GP2: { y: <bool>, predicted_mechanism: "<>" }
  GP3: { y: <bool>, offending_sections: [] }
  GP4: { y: <bool>, voice_instances: [] }
  GP5: { y: <bool>, template_repetition: "<>" }
  GP6: { y: <bool>, surprise_moment: "<>" }
  GP7: { y: <bool>, qa_pattern_evidence: "<>" }
  GP8: { y: <bool>, topic_sentence_chain: [] }
round_pass: <bool>
minimum_fix: |
  <ordered list of fixes the author must apply before the next round>
```

## 6. Aggregation rule

`round_pass = true` iff:

- Every `U_i` (U1–U10) has `triggered: false`
- Every `P_i` BAN row (P1–P5) has `triggered: false`
- Every `P_i` DISC row (P6–P9) has `y: true`
- Every `X_i` (X1–X9) has `y: true`
- Each of the 9 rubric files has `pass: true`: `abstract.md`, `introduction.md`, `motivation.md`, `design.md`, `implementation.md`, `evaluation.md`, `related-work.md`, `conclusion.md`, `typography.md`
- ≥ 6 of 8 `GP_i` have `y: true`

Anything less than full `round_pass` returns `minimum_fix` listing the specific changes required.
