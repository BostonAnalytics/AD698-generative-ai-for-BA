# Compass presentation theme

An opt-in Reveal.js theme adapted from the supplied `marketing-mockup.html` reference. The trial is `M2/M02_P2.qmd`. The original `presentation.scss` remains available for other decks.

Use this configuration in a module presentation:

```yaml
format:
  revealjs:
    theme: [default, ../theme/compass.scss]
    width: 1280
    height: 720
    margin: 0.08
    center: false
    transition: fade
    auto-stretch: false
title-slide-attributes:
  data-background-color: "#111820"
```

Remove the old title background image when adopting the theme. Typography uses Inter when installed, then the system sans-serif stack, without a network font dependency. Colors follow the reference: charcoal `#111820`, warm white `#f7f7f5`, crimson `#a81d2a`, teal `#0f7188`, and muted text `#5d6774`.

Use regular Quarto columns for text beside diagrams. Add `.figure-only` to slides dominated by a large figure, and `.paired-diagrams` when two diagrams sit below introductory bullets. Keep long code examples on separate slides at meaningful boundaries.

For comparison cards, use a `.compass-cards` fenced div containing three `.compass-card` divs. Use `[Card title]{.card-heading}` inside each card. A Markdown heading inside a card can cause Pandoc to generate a nested Reveal section, so use the styled span instead.

Render with `quarto render M2/M02_P2.qmd --to revealjs`. Review both the normal deck and `?print-pdf` view for missing images, math errors, overflow, and code scrollbars before applying the theme to another deck.
