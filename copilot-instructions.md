# Copilot Instructions for AD698 GenAI Course

## Project Overview
This is a **Quarto-based course website** for AD 698 Applied Generative AI Business Analytics. The site contains lecture notes, labs, presentations, assignments, and project milestones organized by modules (M00-M07).

## Architecture & Structure

### Module Organization
- **8 modules** (M00-M07) each containing standardized content types:
  - `M##_LN01.qmd`, `M##_LN02.qmd` - Lecture Notes
  - `M##_P01.qmd`, `M##_P02.qmd` - Presentations (RevealJS slides)
  - `M##_Lab01.qmd`, `M##_Lab02.qmd` - Lab activities
  - `M##_A.qmd` - Assignments
  - `M##_Proj.qmd` - Project milestones
  - `M##_Highlights.qmd`, `M##_Wrapup.qmd` - Module summaries

### Key Configuration Files
- `_quarto.yml` - Main site configuration (port 4300, no navbar, Jupyter engine)
- `requirements.txt` - Python dependencies for Jupyter notebooks
- `data/AD698-Schedule.xlsx` - Course schedule/grading data source
- `theme/metanalytics.scss` - Custom styling (Merriweather font, APA-style headings)

## Content Conventions

### YAML Front Matter Standards
All `.qmd` files use consistent metadata:
```yaml
---
title: "M##: Type Title"
subtitle: "Specific topic description"
number-sections: true
date: "2024-11-21"
date-modified: today
date-format: long
engine: jupyter
categories: ['Type', 'M##:', 'Number']
description: "Brief description."
---
```

**Presentations** add specific format overrides:
```yaml
format:
  revealjs:
    theme: [../analytics_themes/presentation.scss]
    html-math-method: mathml
    slide-number: c/t
  pptx:
    reference-doc: ../analytics_themes/AD688_Presentation.pptx
```

### Naming Conventions
- Module prefixes: `M00` through `M07`
- File types: `LN` (Lecture Notes), `P` (Presentation), `Lab`, `A` (Assignment), `Proj` (Project)
- Sequential numbering: `01`, `02` for multiple items of same type

## Development Workflow

### Building the Site
```powershell
quarto preview  # Live preview on port 4300
quarto render   # Build to _site/ directory
```

### Python Environment
- Use Jupyter kernel with dependencies from `requirements.txt`
- Key packages: pandas, jupyter, bokeh, plotly, langchain, chromadb, faiss

### Data Integration Pattern
The `index.qmd` demonstrates the standard pattern for embedding Excel data:
```python
import pandas as pd
from IPython.display import display, HTML

df = pd.read_excel("data/AD698-Schedule.xlsx", sheet_name="SheetName")
styled = df.style.hide(axis="index").set_table_styles([...])
display(HTML(styled.to_html()))
```

## Style Guidelines

### Typography
- Headings: APA-style formatting in `#003366` color
- Font: Merriweather serif at 12pt base
- Heading sizes: h1=16pt, h2=15pt, h3=14pt (italic), h4=13pt (italic), h5=12pt

### Code Blocks
- Use `{python}` for executable Jupyter cells
- Common cell options: `#| echo: false`, `#| output: html`

## Important Notes
- **No navbar**: Navigation disabled by default (see `_quarto.yml` commented section)
- **Render on save**: Enabled for rapid iteration
- **Embed resources**: HTML files are self-contained
- **Freeze execution**: Set to `false` - notebooks execute on every render
- **Git ignore**: `/.quarto/` and `**/*.quarto_ipynb` (temporary Jupyter conversion files)

## When Creating New Content
1. Copy appropriate template from existing module (e.g., `M01_Lab01.qmd`)
2. Update YAML front matter with correct module number, title, subtitle
3. Adjust `categories` to match content type
4. For presentations, ensure `format: revealjs` section is included
5. Place in correct `M##/` directory
6. Python code cells should follow the pandas → styled table → HTML display pattern
