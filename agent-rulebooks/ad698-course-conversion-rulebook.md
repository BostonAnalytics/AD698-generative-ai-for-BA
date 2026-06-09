# AD698-Style Course Conversion Rulebook

Use this rulebook to convert arbitrary instructor-provided source material into a Quarto course structure modeled on AD698. The goal is to preserve the instructor's intellectual intent while producing a consistent set of module folders, slide decks, lecture notes, highlights, and wrap-ups that can render as a Quarto website.

## Mission

Given course source files such as PowerPoint decks, LaTeX Beamer files, PDFs, Word documents, existing Markdown, notebooks, syllabi, or mixed folders, produce a coherent AD698-like course in QMD.

The canonical conversion target is:

```text
M1/
  M01_P1.qmd
  M01_LN1.qmd
  M01_P2.qmd
  M01_LN2.qmd
  M01_highlights.qmd
  M01_Wrapup.qmd
M2/
  M02_P1.qmd
  M02_LN1.qmd
  M02_P2.qmd
  M02_LN2.qmd
  M02_highlights.qmd
  M02_Wrapup.qmd
...
```

For a 12-presentation source course, default to 6 modules with 2 presentations per module unless the syllabus or source sequence clearly implies a different grouping.

## Agent Roles

Use these roles as separate agents or as explicit stages in one Codex workflow.

### 1. Intake Agent

Responsibilities:

- Inventory all provided files.
- Identify source type, order, dependencies, images, speaker notes, bibliography, and instructor metadata.
- Extract a normalized source manifest.
- Flag unreadable, duplicate, missing, or ambiguous files before conversion.

Output:

```yaml
course_title:
instructor:
source_files:
  - path:
    type: pptx | beamer | pdf | docx | md | qmd | ipynb | other
    inferred_order:
    title:
    slide_count:
    has_speaker_notes:
    assets:
module_plan:
  - module: 1
    title:
    sources:
      - source_file:
        target_presentation: M01_P1.qmd
        target_notes: M01_LN1.qmd
conversion_risks:
```

### 2. Extraction Agent

Responsibilities:

- Convert source files into structured intermediate content.
- Preserve slide titles, bullets, figures, tables, equations, citations, speaker notes, and code blocks.
- Extract images to stable asset folders beside the target QMD files.
- Recover math and tables as structured Markdown or Quarto-compatible code.

Recommended backend:

- Use Mathpix or an equivalent OCR/math parser for scanned PDFs, equation-heavy decks, and Beamer PDFs.
- Use native parsers when available:
  - `python-pptx` or LibreOffice export for PPTX.
  - LaTeX parser plus Pandoc for Beamer `.tex`.
  - Pandoc for Word, Markdown, and LaTeX where feasible.
  - Notebook conversion through `quarto convert` or `jupyter nbconvert` when appropriate.

Intermediate representation:

```yaml
source_id:
title:
sections:
  - heading:
    slides:
      - slide_number:
        title:
        body_blocks:
          - type: text | bullets | table | figure | equation | code | quote
            content:
            source_location:
        speaker_notes:
        assets:
        citations:
```

### 3. Module Architect Agent

Responsibilities:

- Group presentations into modules.
- Assign module titles, lecture titles, and learning arcs.
- Preserve original ordering unless there is strong evidence that regrouping improves coherence.
- Make each module contain:
  - one `M##_highlights.qmd`
  - one `M##_Wrapup.qmd`
  - one `M##_P#.qmd` per presentation
  - one `M##_LN#.qmd` per presentation

Default grouping rules:

- 12 source presentations -> 6 modules x 2 presentations.
- 8 source presentations -> 4 modules x 2 presentations.
- 10 source presentations -> 5 modules x 2 presentations.
- If the number is odd, place the extra presentation in the most conceptually dense module or create a short bridge module.
- If the source contains a syllabus schedule, prefer its week/module boundaries over numeric grouping.

Module design rules:

- Each module should have a coherent business analytics or applied AI theme.
- The first presentation should usually introduce concepts and vocabulary.
- The second presentation should usually deepen the workflow, tool use, implementation pattern, evaluation method, or case application.
- Do not invent a new course arc that contradicts the source. Improve structure, not authorship.

### 4. Slide Deck Conversion Agent

Responsibilities:

- Generate presentation QMD files with RevealJS front matter.
- Convert source slides into polished Quarto slides.
- Preserve figures and tables.
- Improve readability while keeping scope faithful.

Target filename:

```text
M#/M##_P#.qmd
```

Required front matter:

```yaml
---
title: "COURSE_TITLE"
subtitle: "LECTURE_TITLE"
logo: "../theme/figures/met_signature_toptier_rgb.png"
date-modified: today
date-format: long
format:
  revealjs:
    theme: [../theme/presentation.scss]
    html-math-method: katex
    slide-number: c/t
    toc: true
    toc-depth: 1
self-contained-math: true
fig-align: center
execute:
  echo: false
  warning: false
  message: false
bibliography: ../references.bib
csl: ../mis-quarterly.csl
categories: []
description: ""
---
```

Slide rules:

- Use `#` for major sections and `##` for individual slides.
- Use `---` to separate slides where needed.
- Keep slide body concise: usually 3-6 bullets or one primary visual plus supporting bullets.
- Use callouts sparingly for key insight, warning, practice guidance, or business interpretation.
- Preserve citations using Quarto citation syntax where possible, for example `[@source]`.
- Add meaningful `fig-alt` to every image.
- Add `fig-align="center"` to every image unless the layout intentionally differs.
- Add stable figure ids when figures are referenced, for example `#fig-m03-p1-transformer-flow`.
- Use relative paths from the QMD file to its local assets.

Figure syntax:

```markdown
![Short descriptive alt text](./M##_lecture##_figures/example.png){width=80% fig-align="center" fig-alt="Short descriptive alt text" #fig-m##-p#-example}
```

### 5. Lecture Notes Agent

Responsibilities:

- Generate long-form lecture notes for each presentation.
- Expand slide bullets into a coherent written explanation.
- Preserve the order and conceptual emphasis of the original deck.
- Add technical intuition, examples, business analytics implications, and transition paragraphs.

Target filename:

```text
M#/M##_LN#.qmd
```

Required front matter:

```yaml
---
title: "COURSE_TITLE"
subtitle: "LECTURE_TITLE"
number-sections: true
date-modified: today
date-format: long
engine: jupyter
bibliography: ../references.bib
categories: []
description: ""
---
```

Lecture note rules:

- Use `#` for main topics and `##` for subtopics.
- Do not merely restate slides. Convert slide intent into teachable prose.
- Include examples and applied interpretation when the source implies them.
- Preserve math in Quarto-compatible LaTeX.
- Include figures when they materially support learning.
- Every figure must include `fig-alt`; every image should be centered unless there is a good reason otherwise.
- Use callouts for conceptual warnings, intuition, or applied takeaways.
- Avoid unsupported factual claims. If the source includes citations, preserve them.

### 6. Highlights Agent

Responsibilities:

- Generate one module-level preview file.
- Summarize the learning arc across all presentations in the module.
- Provide lecture-specific highlights and learning objectives.
- Add an applied bridge that explains how students should connect concepts to assignments, labs, notebooks, or business cases.

Target filename:

```text
M#/M##_highlights.qmd
```

Recommended structure:

```markdown
---
title: "COURSE_TITLE"
subtitle: "MODULE_TITLE"
number-sections: true
date-modified: today
date-format: long
categories: []
description: ""
---

# Lecture #.1: LECTURE_TITLE

## Highlights

- ...

## Learning Objectives

By the end of this lecture, students will be able to:

- ...

---

# Lecture #.2: LECTURE_TITLE

## Highlights

- ...

## Learning Objectives

By the end of this lecture, students will be able to:

- ...

## Applied Code Bridge

- ...
```

### 7. Wrap-Up Agent

Responsibilities:

- Generate one module-level synthesis file.
- Help students consolidate what they learned.
- Add a consistency check before assignments or projects.
- Preview the next module.

Target filename:

```text
M#/M##_Wrapup.qmd
```

Recommended structure:

```markdown
---
title: "COURSE_TITLE"
subtitle: "MODULE_TITLE"
number-sections: true
date-modified: today
date-format: long
categories: []
description: ""
---

# What We Learned

- ...

# Consistency Check Before Submission

- ...

# Preparing for Module NEXT

- ...
```

## Source-Type Conversion Rules

### PowerPoint

- Extract slide title, ordered text boxes, tables, images, speaker notes, and embedded media.
- Preserve visual order by reading layout positions.
- Convert speaker notes into lecture-note expansion material, not slide clutter.
- Export complex diagrams as images if textual reconstruction would distort meaning.
- Rebuild simple tables directly in Markdown.

### LaTeX Beamer

- Convert frame titles to `##` slide headings.
- Preserve section commands as `#` headings.
- Preserve equations as LaTeX.
- Convert TikZ or complex diagram environments to images unless the target repo already supports the required extensions.
- Convert BibTeX references into `references.bib` entries when present.

### PDF

- If generated from slides, infer slide boundaries by page.
- If scanned or equation-heavy, use Mathpix-style OCR.
- Extract figures to assets and add alt text based on visible content.
- Validate extracted math manually or with a reviewer pass.

### Word or Markdown

- Infer module and lecture boundaries from headings.
- Convert dense prose into notes first, then derive slides.
- Preserve tables, citations, and references.

### Notebook

- Preserve executable code only if it is part of instruction.
- Convert narrative cells into lecture notes.
- Convert compact explanations and key outputs into slides.
- Keep long code walkthroughs in lab or tutorial files if the course structure supports them.

## Quality Bar

The converted course is acceptable only when:

- All target QMD files exist for the planned modules.
- Every source presentation maps to exactly one presentation QMD and one lecture note QMD.
- Module highlights and wrap-ups are present.
- Quarto renders without fatal errors.
- Images have relative paths, `fig-alt`, and `fig-align="center"` where appropriate.
- Notes expand the original material without changing the instructor's intent.
- Generated module titles and learning objectives match the source content.
- No source file is silently dropped.

## Evaluation Metrics

Use these metrics to compare conversion agents or prompt systems:

| Metric | Meaning | Target |
|---|---|---|
| Source coverage | Percent of source slides/sections represented in target files | >= 95% |
| Structure accuracy | Correct module, presentation, notes, highlights, wrap-up files | 100% |
| Render success | Quarto render completes without fatal errors | 100% |
| Figure compliance | Images include stable paths, alt text, and alignment | >= 98% |
| Notes usefulness | Notes explain rather than merely copy slides | Human review pass |
| Fidelity | No major invented claims or omitted core topics | Human review pass |
| Issue count after review | Number of publishing or structural issues found | Lower is better |

## Standard Codex Workflow

1. Inspect the repository structure and `_quarto.yml`.
2. Inventory source files and create `conversion_manifest.yml`.
3. Build the module plan.
4. Convert one pilot module.
5. Render or dry-run the pilot module.
6. Run the reviewer rulebook on the pilot.
7. Fix repeatable conversion mistakes.
8. Convert the remaining modules.
9. Run full reviewer pass.
10. Produce a final report with created files, source coverage, unresolved risks, and render status.

## Final Report Template

```markdown
# Course Conversion Report

## Summary

- Source files processed:
- Modules created:
- Presentations created:
- Lecture notes created:
- Highlights created:
- Wrap-ups created:

## Source Coverage

| Source | Target Presentation | Target Notes | Status |
|---|---|---|---|

## Render Status

- Command:
- Result:
- Errors:
- Warnings:

## Reviewer Findings

- Critical:
- Major:
- Minor:

## Remaining Human Decisions

- ...
```
