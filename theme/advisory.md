# Advisory presentation theme

`advisory.scss` adapts the supplied `advisory-board-overview.html` design for Quarto Reveal.js. The theme is used by all 22 module presentations (M0 through M8, including the instructor introduction) and the timeline helper. M2/M02_P2.qmd is the reference example. It uses white slides, compact crimson branding, dark sans-serif headings, soft gray comparison cards, teal secondary text, and a ruled footer. The course wordmark replaces the reference's unavailable `advisory-board-mark.png`.

Use the existing M02_P2 YAML as the configuration example. The theme entry is `[default, ../theme/advisory.scss]`, the title background is `#ffffff`, and the slide dimensions are 1280 by 720. Keep the footer specific to the deck. Image layout helpers and `.compass-cards`/`.compass-card` markup are compatible with the previous trial.

To return to the earlier style, select `[default, ../theme/compass.scss]`, change the title background to `#111820`, and remove the advisory footer setting. Both theme files remain available. Use only one of these custom themes at a time.

Render decks serially, then check both the normal slideshow and `?print-pdf`. In particular, confirm that the title, logo, footer, comparison cards, formulas, and code fit at the final slide dimensions.


## Course rollout

Each Reveal.js document selects the shared theme explicitly so lecture notes, assignments, and the course website retain their own HTML format. New presentations should copy the Reveal.js settings from M2/M02_P2.qmd, keep a deck-specific footer, and use the repository BU wordmark. The standard frame is 1280 by 720, with a 0.08 margin and top-aligned content.

Legacy emphasis classes (`uublue-bold`, `uugreen-bold`, `uured-bold`, and `bloodred-bold`), references, code annotations, and timeline embeds are supported. Multiple authors stack within the title panel. Avoid combining the old `presentation.scss` with this theme.

The M7/M8 exclusions in the website configuration are independent of the theme: those presentation sources adopt the theme without changing which modules the normal website build publishes.

Use `.compact-table` for dense full-width tables and `.code-detail` for short instructional code steps. Split longer examples at logical boundaries instead of relying on scrollable code boxes. The shared theme limits Mermaid diagram height to keep diagrams within the presentation frame.
