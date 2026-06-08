# Implementation — Section Reference

> Author: apply §1–5 while drafting. Reviewer (auto-review-loop): apply §6 Reviewer Rubric, emit §7 YAML.

## 1. Role

§4 explains how the design of §3 was actually built: language, scale, key engineering decisions, and where the artifact lives. §4 is the shortest body section in a systems paper and the easiest to write badly. **It is implementation, not interface.** APIs, function signatures, file layouts, JSON schemas, configuration knobs, and CLI flags belong in an artifact README or an appendix — not in the paper body.

The reader of §4 leaves knowing what the system is built in, how big it is, what existing systems it stands on, and which engineering choices mattered. The reader does not learn any file path, any function name, or any directory layout.

## 2. Required components

| ID  | Cat  | Component                   | Content                                                                                                           |
| --- | ---- | --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| L1  | COMP | Language and framework      | Language (with version if relevant), key frameworks the implementation builds on.                                 |
| L2  | COMP | Scale                       | Total LOC for the implementation. Optionally split into 2–3 named sub-components by *role* (e.g., "transport layer", "session manager") — not by file. |
| L3  | COMP | Key engineering decisions   | One or two engineering choices worth naming — choices that affected performance, simplicity, or correctness, but were not previously described in §3. |
| L4  | COMP | Dependency                  | One sentence on what existing systems or libraries the implementation depends on or extends.                       |
| L5  | COMP | Artifact pointer            | One sentence at the end (or one footnote) pointing to the code release / repo / artifact. Anonymized if pre-decision. |

## 3. Prose discipline

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| L6  | DISC | Length: 0.5–1.0 page. More than 1.0 page means §4 has absorbed material that belongs in §3 or §5.             |
| L7  | DISC | Components are named **semantically** (the calibration extractor, the kernel scheduler, the framework-overhead microbench), not by file path. The reader must be able to follow §4 without ever learning a file name. |
| L8  | DISC | LOC counts appear at most three times in §4: once for the total, optionally once each for the two largest sub-components.                                                              |
| L9  | DISC | If a file path is genuinely essential for the reader to reproduce a result, it goes in a footnote — never in body text. Limit: one such footnote in §4. |
| L10 | DISC | §4 paragraphs are continuous prose. The section is not a file-by-file walkthrough. Its paragraph structure mirrors the *system's architecture*, not the *directory tree*. |
| L11 | DISC | Function names, class names, JSON keys, configuration-knob names, CLI flag names, and command-line invocations belong to the artifact README or to an appendix. |
| L12 | DISC | LOC counts are reported as natural numbers (4,000 / 20,000 / 25K), not as audit-trail precision (584, 412, 256, 188). Audit-trail precision reads as inventory; natural-number precision reads as scale. |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| L13 | BAN | A file path or filename appears in §4 body text (anything matching `*.py`, `*.cpp`, `*.cu`, `*.json`, `*.h`, `*.sh`, `*.tex`, `*.yaml`, `*.toml`, or containing a `/` other than in a URL). Footnotes are permitted; body text is not. |
| L14 | BAN | More than three distinct LOC counts appear in §4. Per-file LOC enumeration is README content.                |
| L15 | BAN | A function name, class name, struct name, JSON key, configuration knob, or CLI flag appears in §4 body.     |
| L16 | BAN | §4 exceeds 1.25 pages. Implementation that needs more space belongs in §3.                                  |
| L17 | BAN | §4 reads as a README — its paragraph structure mirrors directory structure (one paragraph per file or one paragraph per module). |
| L18 | BAN | §4 documents the artifact interface: how to run the code, what flags to pass, what schema is expected.       |
| L19 | BAN | A `\texttt{...}` or `\path{...}` block containing a filename or directory name appears in §4 body text.     |

## 5. Worked exemplar (Homa-style)

A strong implementation section reads at the system level. Homa's §4 occupies roughly one column. It reports that Homa is implemented as a Linux kernel transport module of approximately 4,000 lines of C, integrated with the netdev queueing API for priority assignment and reusing the existing TCP/IP fallback path for peers that do not support the protocol. It names one engineering decision worth recording — how the kernel module avoids per-packet allocations on the priority path — and ends with a one-sentence pointer to the open-source release.

What Homa's §4 does not contain: any file name, any per-file LOC count, any function or structure name, any compile or run instruction. All of that lives in the kernel-module README and the upstream Linux tree.

eRPC takes the same shape. The §4 reports that eRPC is implemented in roughly 20,000 lines of C++, structured into a transport layer that abstracts over DPDK and InfiniBand verbs and a session manager that handles connection state. One engineering decision is named (the lock-free transmit path) with one sentence on why it was chosen. The artifact URL is in a footnote.

When drafting your own §4, write at this level. Name the language, the scale, the dependencies, one or two engineering choices that mattered, and the artifact pointer. Everything else is README content.

## 6. Reviewer Rubric

Apply each row Y/N from §4 text alone. **Pass = every COMP and DISC row Y, every BAN row not triggered.**

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| L1  | COMP | Language and framework named                                                                | Quote the sentence                                                             |
| L2  | COMP | Total LOC stated                                                                            | Quote                                                                          |
| L3  | COMP | 1–2 key engineering decisions named                                                         | Quote each                                                                     |
| L4  | COMP | Dependency on existing systems/libraries named                                              | Quote                                                                          |
| L5  | COMP | Artifact pointer present                                                                    | Quote                                                                          |
| L6  | DISC | Length in [0.5, 1.0] page                                                                   | Report page count                                                              |
| L7  | DISC | All components named semantically; reader can follow §4 without learning a file name        | List the semantic names used; confirm zero file names                          |
| L8  | DISC | LOC counts ≤ 3 in §4                                                                        | Count                                                                          |
| L9  | DISC | ≤ 1 file-path footnote                                                                      | Count                                                                          |
| L10 | DISC | §4 is continuous prose; paragraph structure mirrors architecture, not directory tree        | Describe paragraph mapping                                                     |
| L11 | DISC | No function / class / JSON-key / CLI-flag names in §4 body                                  | List offenders                                                                 |
| L12 | DISC | LOC counts use natural-number precision                                                     | List counts; classify "natural" vs "audit-trail"                               |
| L13 | BAN  | No file paths or filenames in §4 body                                                       | Grep for `*.py`, `*.cpp`, `*.cu`, `*.json`, `*.h`, `*.sh`, `*.tex`, `*.yaml`, `/` |
| L14 | BAN  | ≤ 3 distinct LOC counts                                                                     | Triggered if count > 3                                                         |
| L15 | BAN  | No code-identifier names in §4 body                                                         | List offenders                                                                 |
| L16 | BAN  | §4 ≤ 1.25 pages                                                                             | Report page count                                                              |
| L17 | BAN  | §4 not README-shaped (paragraph ↔ file/module mapping)                                      | Describe mapping; flag if 1:1 with files                                       |
| L18 | BAN  | §4 does not document artifact interface (no run instructions / flag descriptions / schemas) | List offenders                                                                 |
| L19 | BAN  | No `\texttt{}` / `\path{}` containing filenames in body                                     | Grep                                                                           |

### Gestalt

| ID  | Cat  | Check                                                                          |
| --- | ---- | ------------------------------------------------------------------------------ |
| GL1 | GEST | A reader of §4 can describe the system at the implementation level — language, scale, key choices, dependencies — without learning any file path or function name |
| GL2 | GEST | §4 reads as a section of a paper, not as a section of a README                 |

## 7. Reviewer YAML output

```yaml
section: implementation
page_count: <float>
loc_counts_in_section: <int>
file_paths_in_body: [<list>]
code_identifiers_in_body: [<list>]
pass: <bool>
comp:
  L1: { y: <bool>, evidence: "<>" }
  L2: { y: <bool>, total_loc: <int> }
  L3: { y: <bool>, decisions: [] }
  L4: { y: <bool>, evidence: "<>" }
  L5: { y: <bool>, evidence: "<>" }
disc:
  L6:  { y: <bool>, value: <float> }
  L7:  { y: <bool>, semantic_names: [], file_names_found: [] }
  L8:  { y: <bool>, count: <int> }
  L9:  { y: <bool>, footnote_count: <int> }
  L10: { y: <bool>, paragraph_mapping: "<>" }
  L11: { y: <bool>, offenders: [] }
  L12: { y: <bool>, classification: [] }
ban:
  L13: { triggered: <bool>, offenders: [] }
  L14: { triggered: <bool>, count: <int> }
  L15: { triggered: <bool>, offenders: [] }
  L16: { triggered: <bool>, value: <float> }
  L17: { triggered: <bool>, mapping: "<>" }
  L18: { triggered: <bool>, offenders: [] }
  L19: { triggered: <bool>, offenders: [] }
gestalt:
  GL1: { y: <bool> }
  GL2: { y: <bool> }
minimum_fix: |
  <ordered edits required to flip pass to true>
```
