# Typography — LaTeX Layout and Overflow Reference

> Universal LaTeX hygiene. Author applies §2–4 while drafting and after every compile. Reviewer (auto-review-loop) applies §5 Rubric, emits §6 YAML.

## 1. Role

Systems venues reject papers that visually overflow column boundaries. Overflow is read by reviewers as carelessness, and the failure mode is universal in LLM-generated drafts because the model emits long non-breakable tokens (file paths, compound subscripts, table cells, URLs) without the LaTeX wrappers that allow line breaking.

This file enumerates the LaTeX patterns that cause overflow and the discipline that prevents it. The companion ban is `whole-paper.md` U10: any `Overfull \hbox` warning > 5pt in `main.log` fails the round.

## 2. Causes and fixes

Long non-breakable tokens force LaTeX to either overflow the column or push the entire line past the margin. The fix is always: insert breakpoints, restructure into display math, or shrink the cell.

| Cause                                                                                    | Fix                                                                                                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| File path or filename in body text (`src/very_long_module_name.py`)                       | Remove. File paths violate `whole-paper.md` U9 in body text. If the path is essential in an appendix, wrap with `\path{...}` (from `url` package) or `\seqsplit{...}` (from `seqsplit` package). |
| Long URL                                                                                 | Wrap with `\url{...}` (from `hyperref` or `url`). Never paste a bare URL into body text.                                                                          |
| Inline math wider than 30% of column width                                               | Promote to display math (`\[ ... \]` or `equation`).                                                                                                              |
| Display math wider than the column                                                       | Break with `aligned`, `multline`, or `align` and explicit `\\` line breaks at natural points (after `=`, after a binary operator, before an open parenthesis).    |
| Long compound subscript inline (`\eta_{\text{long_word}}(\text{arch}, T, K, N)`)         | Define a short alias once (`\eta_p := \eta_{\text{proj}}`) and use the alias inline. Or promote the expression to display math.                                   |
| Long inline code identifier (`\texttt{very_long_identifier_name}`)                       | Identifiers do not belong in body text (U9). If essential in an appendix, use `\texttt{}` with `\seqsplit{}` or shorten via semantic naming.                      |
| Long table cell content (`compute/memory/dispatch/framework`)                            | Use `\makecell{compute / memory \\ dispatch / framework}` for manual line break, OR shorten to two cells, OR shorten the term itself.                             |
| Table wider than `\columnwidth`                                                          | Restructure (drop columns / collapse rows) is preferred. As last resort, switch to `\begin{table*}` (two-column float) or `\resizebox{\columnwidth}{!}{...}`.      |
| Inline equation containing many fractions or large operators                             | Promote to display math.                                                                                                                                          |

## 3. Required practices

| ID  | Cat  | Rule                                                                                                          |
| --- | ---- | ------------------------------------------------------------------------------------------------------------- |
| T1  | DISC | After every `pdflatex` run, grep `main.log` for `Overfull \hbox`. Treat warnings > 5pt as build errors. Recompile until zero remain. |
| T2  | DISC | URLs use `\url{...}`. Long identifiers in the appendix use `\path{...}` or `\texttt{}` with `\seqsplit{...}`.   |
| T3  | DISC | Inline math expressions wider than 30% of column width are promoted to display math.                          |
| T4  | DISC | Display math wider than `\columnwidth` (single-column layout) or `\textwidth` (two-column layout `\begin{equation*}` in a starred float) is broken with `aligned`, `multline`, or `align`. |
| T5  | DISC | Table cells whose rendered width exceeds the available column are restructured: shorter content, `\makecell{... \\ ...}`, or split into two cells. |
| T6  | DISC | Tables wider than the surrounding `\columnwidth` / `\textwidth` are restructured before resorting to `\resizebox`. |
| T7  | DISC | Long compound subscripts inside inline math are aliased once and the alias is used thereafter.                |

## 4. Hard bans

| ID  | Cat | Banned pattern                                                                                              |
| --- | --- | ----------------------------------------------------------------------------------------------------------- |
| T8  | BAN | Any `Overfull \hbox` warning > 5pt in `main.log` (also enforced as universal U10).                          |
| T9  | BAN | A bare long token (file path, URL, identifier, > 20 characters with no break point) appears in body text without `\path{}`, `\url{}`, or `\seqsplit{}`. |
| T10 | BAN | An inline math expression visibly extends past the column boundary in the rendered PDF.                     |
| T11 | BAN | A table cell or table row visibly exceeds the surrounding column or page width.                             |
| T12 | BAN | A long compound subscript (`\eta_{\text{long_word}}(\text{arch}, T, K, N)`) appears in inline math (only). The same expression in display math is fine. |
| T13 | BAN | A figure or table is placed in a single-column float (`figure`, `table`) but its content requires two-column width. Use `figure*` / `table*`. |

## 5. Verification procedure

**Author** (after every compile):

1. Run `pdflatex main.tex` (twice or three times to settle references).
2. `grep -n "Overfull \\\\hbox" main.log` and inspect every warning.
3. For each warning > 5pt, the log reports the offending source line range. Apply the matching fix from §2.
4. Recompile. Repeat until zero warnings > 5pt.
5. Open the PDF. Visually scan each column for content that breaches the margin (text, equation, table rule, figure edge).

**Reviewer** (auto-review-loop):

1. Require the author to attach `main.log` to the round artifact set.
2. Parse `main.log` for `Overfull \hbox` warnings; record max overflow in points.
3. Parse `main.tex` for the hygiene patterns in §3 (presence of `\url{}` around URLs, `\path{}` around file references, `aligned`/`multline` around wide display math, `\makecell` in wide table cells).
4. If the rendered PDF is accessible, visually verify the absence of visible overflow.
5. Emit the §6 YAML output.

## 6. Reviewer Rubric

| ID  | Cat  | Check                                                                                       | How to verify                                                                  |
| --- | ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| T1  | DISC | `main.log` has zero `Overfull \hbox` warnings > 5pt                                         | Grep `main.log`                                                                |
| T2  | DISC | Every URL in the paper is wrapped with `\url{}`                                             | Grep `.tex` for bare `http://` / `https://` outside `\url{}`                   |
| T3  | DISC | No inline math wider than ~30% of column width                                              | Inspect inline math; flag suspicious expressions                               |
| T4  | DISC | All wide display math is broken with `aligned` / `multline` / `align`                       | Inspect display math environments                                              |
| T5  | DISC | Wide table cells use `\makecell` / restructured / shortened                                 | Inspect each table                                                             |
| T6  | DISC | Tables fit within `\columnwidth` / `\textwidth` without `\resizebox` where possible         | Inspect each table                                                             |
| T7  | DISC | Long compound subscripts are aliased before being used inline                               | Inspect math macros                                                            |
| T8  | BAN  | No `Overfull \hbox` > 5pt                                                                   | Triggered if any present                                                       |
| T9  | BAN  | No bare long token in body text                                                             | List offenders                                                                 |
| T10 | BAN  | No inline math extending past column                                                        | List offenders                                                                 |
| T11 | BAN  | No table overflow                                                                           | List offenders                                                                 |
| T12 | BAN  | No long compound subscript in inline math                                                   | List offenders                                                                 |
| T13 | BAN  | No two-column-width content in single-column floats                                         | List offenders                                                                 |

## 7. Reviewer YAML output

```yaml
section: typography
overfull_hbox_warnings_total: <int>
overfull_hbox_warnings_over_5pt: <int>
overfull_hbox_max_pt: <float>
pass: <bool>
disc:
  T1: { y: <bool>, warning_count: <int>, max_pt: <float> }
  T2: { y: <bool>, bare_urls: [] }
  T3: { y: <bool>, oversized_inline_math: [] }
  T4: { y: <bool>, unbroken_wide_display_math: [] }
  T5: { y: <bool>, wide_table_cells: [] }
  T6: { y: <bool>, tables_using_resizebox: [] }
  T7: { y: <bool>, unaliased_long_subscripts: [] }
ban:
  T8:  { triggered: <bool>, max_pt: <float>, count: <int> }
  T9:  { triggered: <bool>, offenders: [{ section: "<>", token: "<>" }] }
  T10: { triggered: <bool>, offenders: [] }
  T11: { triggered: <bool>, offenders: [] }
  T12: { triggered: <bool>, offenders: [] }
  T13: { triggered: <bool>, offenders: [] }
minimum_fix: |
  <ordered edits required to bring main.log to zero overfull warnings > 5pt and to fix any rendered overflow>
```
