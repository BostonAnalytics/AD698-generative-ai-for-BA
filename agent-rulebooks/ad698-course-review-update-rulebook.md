# AD698-Style Course Review and Update Rulebook

Use this rulebook after conversion or course edits. The reviewer agent should find publishing, accessibility, structural, pedagogical, and render problems. The updater agent should make scoped fixes, then re-run the relevant checks.

## Mission

Review AD698-like Quarto course modules and generate actionable issues. When authorized to update, apply fixes that preserve instructor intent and improve render quality, accessibility, consistency, and student usability.

The reviewer should focus on concrete defects rather than stylistic preferences.

## Agent Roles

### 1. Repository Orientation Agent

Responsibilities:

- Inspect `_quarto.yml`, module folders, theme paths, bibliography paths, and render exclusions.
- Identify canonical naming and front matter conventions.
- Detect whether the repo is a website, book, or mixed Quarto project.
- Produce a short repo contract before reviewing.

Repo contract template:

```yaml
quarto_project_type:
module_folders:
presentation_pattern:
lecture_notes_pattern:
required_module_files:
  - highlights
  - Wrapup
theme_paths:
bibliography_paths:
render_scope:
```

### 2. Publishing Reviewer Agent

Responsibilities:

- Inspect QMD syntax, front matter, image attributes, links, citations, references, and code chunks.
- Run Quarto render when feasible.
- Generate issues with severity and file/line references.

### 3. Accessibility Reviewer Agent

Responsibilities:

- Verify image alt text.
- Check headings are hierarchical.
- Flag link text such as "click here".
- Flag figures without captions or meaningful descriptions.
- Check tables for readable headers.

### 4. Pedagogy Reviewer Agent

Responsibilities:

- Check whether slides and notes align.
- Flag lecture notes that only repeat slides.
- Check whether module highlights and wrap-ups match module content.
- Flag missing learning objectives, missing applied bridge, or weak module synthesis.

### 5. Update Agent

Responsibilities:

- Fix issues only within the requested scope.
- Preserve course voice, topic order, citations, and file naming.
- Avoid broad rewrites unless the issue requires them.
- Re-run relevant checks after edits.

## Severity Levels

Use these issue levels:

| Severity | Meaning |
|---|---|
| Critical | Blocks render, breaks navigation, deletes source coverage, or creates materially wrong course content |
| Major | Likely publishing/accessibility failure or student-facing confusion |
| Minor | Polish issue, weak consistency, or low-risk improvement |
| Info | Useful observation, not a required change |

## Required File Structure Checks

For each module folder:

- Folder name should be `M#`, for example `M5`.
- Presentation files should follow `M##_P#.qmd`, for example `M05_P1.qmd`.
- Lecture notes should follow `M##_LN#.qmd`, for example `M05_LN1.qmd`.
- Module preview should be `M##_highlights.qmd`.
- Module synthesis should be `M##_Wrapup.qmd`.
- Each `P#` should have a corresponding `LN#`.
- There should be no orphan lecture notes without matching presentations.
- Numbering should be stable and gap-free unless there is a documented reason.

## Front Matter Checks

### Presentation QMD

Required or expected keys:

```yaml
title:
subtitle:
date-modified: today
date-format: long
format:
  revealjs:
    theme:
    html-math-method: katex
    slide-number: c/t
    toc: true
self-contained-math: true
fig-align: center
execute:
  echo: false
  warning: false
  message: false
bibliography:
csl:
categories:
description:
```

Flag:

- Missing `format: revealjs` for presentation files.
- Missing `fig-align: center` globally or on image attributes.
- Missing `self-contained-math: true` when math appears in slides.
- Missing `bibliography` when citations appear.
- Broken relative paths to theme, logo, bibliography, or CSL.
- Empty or generic descriptions such as "Lecture slides".

### Lecture Notes QMD

Required or expected keys:

```yaml
title:
subtitle:
number-sections: true
date-modified: today
date-format: long
bibliography:
categories:
description:
```

Flag:

- Missing `number-sections: true`.
- Missing `engine: jupyter` when executable Python/R code chunks appear.
- Missing bibliography when citations appear.
- Description that does not describe the learning purpose.

## Figure and Asset Checks

For every Markdown image:

```markdown
![caption or alt](path){width=80% fig-align="center" fig-alt="meaningful description" #fig-id}
```

Flag:

- Missing alt text in the Markdown image label.
- Missing `fig-alt`.
- Empty, generic, or repeated `fig-alt`, such as "image", "figure", "diagram", or "screenshot".
- Missing `fig-align="center"` unless intentionally left aligned.
- Broken relative path.
- Absolute local path.
- Image path pointing outside the repo.
- Missing figure id when the figure is referenced elsewhere.
- Duplicate figure ids.
- Width values that are invalid or likely too large for slides.

Update rules:

- Add `fig-alt` using a concise description of what the image communicates.
- Do not invent details not visible or not supported by nearby text.
- Prefer `width=70%` to `width=85%` for slides unless the figure needs close inspection.
- Keep images in module-local asset folders when possible.

## Citation and Bibliography Checks

Flag:

- Citation syntax like `[@key]` with no matching entry in `references.bib`.
- Raw URLs used where a citation or footnote would be better.
- Broken bibliography path.
- Claims in notes that appear to be generated additions without source grounding.
- Duplicate bibliography entries with conflicting metadata.

Update rules:

- Preserve existing citation keys when possible.
- If adding a citation key, add or request a matching BibTeX entry.
- Use footnotes for informal web references when the course does not require formal citation.

## Link Checks

Flag:

- Broken relative links.
- Links to missing QMD files.
- Raw external URLs in body text.
- Ambiguous link text such as "here" or "this".
- Links to generated `_site` or `_freeze` files from source QMD.

Update rules:

- Prefer relative links to source QMD files, not rendered HTML.
- Use descriptive link text.

## Quarto Syntax Checks

Flag:

- Unclosed fenced code blocks.
- Unclosed callout blocks.
- Malformed Div syntax.
- YAML indentation errors.
- Mixed smart quotes in YAML.
- Slide separators in lecture notes when not intended.
- Tables with uneven columns.
- Mermaid, LaTeX, or HTML blocks unsupported by the configured format.

Update rules:

- Make the smallest syntax fix that preserves content.
- Re-render the affected file or project section after syntax fixes.

## Code Chunk Checks

Flag:

- Code chunks with missing language identifiers.
- Code that depends on paths outside the repo.
- Code chunks in slides that should not execute.
- Missing `execute` controls when code is demonstration-only.
- Errors hidden by overly broad settings when the file is intended as a lab.

Update rules:

- In presentation files, default to non-noisy execution:

```yaml
execute:
  echo: false
  warning: false
  message: false
```

- In labs or tutorials, preserve visible code when pedagogically important.
- Do not change analytical results without verifying the notebook or data flow.

## Pedagogical Alignment Checks

For each `M##_P#.qmd` and `M##_LN#.qmd` pair, verify:

- Same lecture topic and title.
- Notes cover all major slide sections.
- Notes explain concepts in prose rather than copying bullets.
- Examples and applications are consistent across slides and notes.
- Figures used in slides are explained in notes when important.
- Key terminology is introduced before use.

For each `M##_highlights.qmd`, verify:

- Each lecture has highlights.
- Each lecture has learning objectives.
- Objectives use observable verbs such as explain, design, implement, evaluate, compare, diagnose, interpret.
- Applied bridge points to concrete course artifacts when available.

For each `M##_Wrapup.qmd`, verify:

- It synthesizes module concepts.
- It includes a consistency check before submission or practice.
- It previews the next module if known.
- It does not introduce substantial new content that students were not taught.

## Issue Output Format

Reviewer agents should emit issues in this format:

```markdown
## Findings

### Critical

- [ ] FILE:LINE - Short issue title
  - Problem: What is wrong.
  - Why it matters: Render, accessibility, correctness, or pedagogy impact.
  - Suggested fix: Specific update.

### Major

- [ ] ...

### Minor

- [ ] ...

## Render Result

- Command:
- Status:
- Relevant output:

## Coverage Notes

- Files reviewed:
- Files skipped:
- Reasons skipped:
```

When using GitHub issues, use this title format:

```text
[Course Review][Major] M05_P1 figure missing fig-alt
```

Recommended issue labels:

```text
course-review
quarto
accessibility
render-blocker
pedagogy
conversion-followup
```

## Update Workflow

1. Read reviewer findings.
2. Group issues by file and root cause.
3. Fix render blockers first.
4. Fix accessibility and publishing issues next.
5. Fix pedagogy alignment issues last.
6. Re-run targeted checks.
7. Run broader render if the edits touched shared configuration or many files.
8. Report exactly what changed and what remains.

## Update Boundaries

The updater may:

- Add missing image attributes.
- Fix broken relative paths.
- Repair front matter.
- Add missing descriptions and categories.
- Repair Quarto syntax.
- Improve weak alt text.
- Align lecture-note headings with slide sections.
- Add concise learning objectives or consistency checks when missing.

The updater must not:

- Rewrite the professor's course argument without request.
- Remove source content because it is hard to convert.
- Delete figures unless they are duplicates or broken and a replacement exists.
- Change grading, assignment instructions, due dates, or policies without explicit approval.
- Modify unrelated modules during a targeted fix.

## Automated Check Ideas

Implement these checks as scripts if the new Codex project will evaluate agents quantitatively:

| Check | Method |
|---|---|
| QMD inventory | Walk `M*/**/*.qmd` and match filename patterns |
| Pairing | Ensure each `M##_P#` has `M##_LN#` |
| YAML validity | Parse front matter with a YAML parser |
| Image attributes | Regex Markdown images and parse attribute blocks |
| Broken paths | Resolve image/link paths relative to each QMD |
| Duplicate figure ids | Collect `#fig-*` ids |
| Citation keys | Compare `[@key]` keys against `.bib` entries |
| Render | Run `quarto render` or targeted `quarto render path.qmd` |
| Notes expansion | Compare section headings and approximate content length against slides |

## Reviewer Scoring Rubric

Use this to evaluate reviewer agents:

| Dimension | Score 0 | Score 1 | Score 2 |
|---|---|---|---|
| Render detection | Misses blockers | Finds some blockers | Finds all obvious blockers |
| Accessibility | Misses image/link issues | Finds common issues | Provides accurate, fixable findings |
| Structure | Misses missing files/pairs | Finds basic naming issues | Fully validates module contract |
| Pedagogy | Only checks formatting | Flags shallow notes/objectives | Evaluates slide-note-module alignment |
| Actionability | Vague comments | Some suggested fixes | Specific file/line fixes |
| False positives | Many | Some | Few |

## Updater Scoring Rubric

Use this to evaluate update agents:

| Dimension | Score 0 | Score 1 | Score 2 |
|---|---|---|---|
| Scope control | Changes unrelated files | Mostly scoped | Strictly scoped |
| Render improvement | Does not improve render | Partially fixes | Resolves targeted blockers |
| Accessibility improvement | Leaves obvious issues | Fixes some | Fixes all targeted issues |
| Fidelity | Alters instructor intent | Minor drift | Preserves intent |
| Verification | No checks | Partial checks | Targeted and reported checks |

## Final Review Report Template

```markdown
# Course Review Report

## Summary

- Files reviewed:
- Critical findings:
- Major findings:
- Minor findings:
- Render status:

## Top Findings

- ...

## Updates Applied

- ...

## Verification

- Command:
- Result:

## Remaining Risks

- ...
```
