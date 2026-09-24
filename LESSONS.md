# Lessons

## 2026-09-22 -- Center native and Quarto float captions with caption-specific theme selectors.
- Reveal slides inherit left alignment. Cover figcaption, .quarto-float-caption, table caption, and legacy p.caption under .reveal .slides; use #quarto-content for HTML notes. Do not center table cells or all paragraph text.
- Both themes compiled with Dart Sass; isolated browser fixtures verified centered figure captions, native table captions, and cross-referenced table captions while table cells remained left-aligned. The language check passed all 42 sources.
- Full M02_P2/M02_LN2 render verification remains incomplete: project discovery failed on missing M0/M0_Lab1_files, then on M0/primers/tokens-and-tokenization_files/figure-pdf during an elevated retry. These are render-discovery failures, not SCSS compilation failures.
- tags: quarto,captions,scss,verification

## 2026-09-22 -- Treat authoring commentary as a delivery failure, including in lecture and presenter notes.
- `python scripts/check_course_language.py` scans all 42 top-level presentation/lecture-note sources in M0 through M8 and initially reports six violations across M02_P1, M02_LN1, M02_LN2, M05_LN1, and M05_LN2. The Quarto pre-render hook invokes the same command; a nonzero result blocks rendering until the source wording is corrected.
- Hidden `.notes`, comments, and image alt text are not safe destinations for authoring rationale. The current AGENTS.md contract supersedes the earlier suggestion to move teaching rationale into presenter notes.
- Verify detection with `python -m unittest discover -s tests -p test_course_language.py`; regression cases cover the reported examples, wrapped/emphasized text, hidden content, and allowed subject explanations. A passing scan does not prove semantic cleanliness or presentation/notes parity: compare slide coverage, figures, and equations and inspect both rendered outputs.
- tags: slides,lecture-notes,authoring-language,acceptance,verification

## 2026-09-22 -- Compute softmax examples over the complete stated outcome set before drawing probability bars.
- For M2/M02_P1.qmd's three scores [2.1, 1.9, 0.1], softmax gives [0.511753, 0.418988, 0.069258]; the prior [0.46, 0.38, 0.02] did not sum to one. Compute with unrounded exponentials and round only the displayed labels.
- The softmax-intuition.svg diagram uses proportional bars within each panel and the slide's existing figure-only class to allow a 460-pixel image; the shared theme otherwise caps slide images at 350 pixels.
- The sentence-based revision expands the toy vocabulary to six words with scores [2.1, 1.9, 1.4, 1.2, 1.0, 0.1]. Its exponential sum is 26.050834 and the rounded percentages total 99.9%; label the rounding instead of changing a probability to force 100%. Recompute the denominator whenever candidates change.
- tags: softmax,quarto,slides,visualization,verification

## 2026-09-17 -- Verify shared Reveal chrome when adapting the advisory theme.
- The advisory reference points to a separate `advisory-board-mark.png` that was unavailable beside the HTML. Reuse the repository's intact BU wordmark rather than shipping the reference's broken image URL.
- Reveal's logo and slide-number positioning needs explicit overrides for the advisory layout: logo at top right, counter at bottom right, with a ruled Quarto footer. Check their positions in slideshow mode as well as `?print-pdf`; page-boundary checks alone do not verify shared chrome.
- `theme/advisory.scss` preserves the Compass layout helpers, so M02_P2 can change themes without rewriting its diagrams or comparison markup. The trial retained 56 slides with no missing images, math errors, page overflow, or vertical code overflow in the browser checks.
- tags: quarto,revealjs,theme,verification

## 2026-09-17 -- Keep comparison-card labels out of Reveal.js heading structure.
- In the Compass presentation trial, Markdown level-three headings inside card divs became nested `section` elements and extra Reveal slides. Use `[Label]{.card-heading}` spans instead, and verify the rendered slide count in the browser.
- Check `?print-pdf` for both page overflow and inner code scrolling. A code block can fit its page while hiding lines in an inner scrollbar. Split long examples at their existing conceptual boundaries and remove decorative comment separators before shrinking code text.
- The reusable theme is `theme/compass.scss`; only `M2/M02_P2.qmd` opts into it. Use a separate theme file for design trials to avoid changing all presentations through `theme/presentation.scss`.
- tags: quarto,revealjs,theme,layout,verification

Written by /aar-loop after each session's After Action Review. Read this file before starting a new task in this project. Every entry should be concrete and checkable, never vague.

## 2026-08-06 -- For AD698 schedule changes, update schedules/config.py and every Quarto schedule cell modality list together; Fall only supports oncampus and o1, so leaving o2 in index.qmd or schedule.qmd breaks render once semester='Fall'. Always render index.qmd and schedule.qmd and inspect _site dates after the change.
- Expected: Switching the syllabus schedule to Fall 2026 would make index.html show Fall dates from the downloaded BU calendar.
- Actual: index.html showed Summer 2026 because schedules/config.py still said Summer; after switching to Fall, the old o2 modality and fixed drop indexes would have broken Fall renders.
- Why: The rendered HTML is produced from Quarto cells that import shared config but keep per-file modality/display assumptions; external module changes and Quarto cache make source and _site output easy to drift unless both affected pages are rendered and inspected.
- tags: quarto,schedule,calendar

## 2026-08-06 -- When scraping https://www.bu.edu/reg/calendars/semester/ for AD698 schedules, read each term from the h3 inside div.bu_collapsible_container and then parse that container's div.bu_collapsible_section table; looking for colspan table headers returns zero rows on this page.
- Expected: Switching the BU downloader to the semester calendar URL would keep load_calendar('Fall', 2026) populated.
- Actual: The first scraper attempt found 25 tables but returned an empty DataFrame because the term labels were h3 headings outside the table rows.
- Why: The semester URL's HTML structure differs from https://www.bu.edu/reg/calendars/: dates live in tables under collapsible containers, while term names live in sibling h3 headings.
- tags: calendar,scraper,bu

## 2026-08-06 -- When verifying multiple Quarto pages in AD698, run quarto render ... serially if they share _site or site_libs; parallel renders can race while copying site_libs/quarto-html/*.js and report PermissionDenied after notebook execution succeeds.
- Expected: Rendering index.qmd, schedule.qmd, and deliverables.qmd in parallel would verify all three pages cleanly.
- Actual: index.qmd and schedule.qmd succeeded, while deliverables.qmd failed with PermissionDenied on site_libs/quarto-html/popper.min.js; rerunning deliverables.qmd serially succeeded.
- Why: Quarto copies shared HTML dependency files into site_libs during render, and simultaneous renders can try to update the same file timestamp on Windows.
- tags: quarto,verification,windows

## 2026-08-06 -- When Quarto render in AD698 fails with NotFound for a missing *.quarto_ipynb_1 cache file, rerun the same page with quarto render <file>.qmd --to html --cache-refresh; do not use --execute-cache-refresh, which this Quarto version passes through to Pandoc as an unknown option.
- Expected: A normal serial quarto render index.qmd --to html would verify the updated schedule page.
- Actual: The first render failed with NotFound for index.quarto_ipynb_1; --execute-cache-refresh executed cells but failed in Pandoc, while --cache-refresh rendered successfully.
- Why: The local Quarto 1.10.18 CLI exposes --cache-refresh; --execute-cache-refresh is not a render option and is treated as a Pandoc argument.
- tags: quarto,verification,cache

## 2026-08-06 -- If AD698 Quarto render still fails with NotFound for *.quarto_ipynb_1 after --cache-refresh, rerun the page with quarto render <file>.qmd --to html --no-cache; this bypasses the stale Jupyter cache pointer without deleting .jupyter_cache.
- Expected: quarto render index.qmd --to html --cache-refresh would recover from the stale notebook cache pointer.
- Actual: The render still failed with NotFound for index.quarto_ipynb_1; quarto render index.qmd --to html --no-cache succeeded, and the same no-cache pattern verified schedule.qmd and deliverables.qmd.
- Why: Quarto can retain a stale reference to an intermediate *.quarto_ipynb_1 file even while refreshing cache metadata; --no-cache forces direct execution for the verification run.
- tags: quarto,verification,cache

## 2026-08-06 -- When AD698 term resolution can advance December renders to Spring of the next year, validate every configured section start_date year against the resolved term year before generating schedules; otherwise Spring 2027 can silently reuse Spring 2026 section dates.
- Expected: Adding a mid-December Spring resolver boundary would make December 15, 2026 generate a Spring 2027 schedule safely.
- Actual: The resolver correctly returned Spring 2027, but the section config currently contains Spring 2026 dates, so generation needed a year-match guard.
- Why: Term selection is automatic by render date, while section start dates are manually configured full ISO dates in section_configs_by_semester.
- tags: schedule,calendar,term-resolution

## 2026-08-09 -- For AD698 Graphify setup, create or tighten .graphifyignore before the first graphify update; if ignore-rule changes intentionally shrink an existing graph, rerun graphify update . --force.
- Expected: Adding MET-style Graphify support would create a clean repo graph from course source files only.
- Actual: The first update scanned generated JSON/data files, then refused to overwrite after .graphifyignore was tightened because the graph would shrink.
- Why: Graphify update is fail-closed when files leave the scan corpus, and this course repo has generated data and outputs outside the initial ignore rules.
- tags: graphify,ignore-rules,workflow

## 2026-08-09 -- When graphify update . fails in AD698 with [WinError 5] Access is denied, retry the same command once with elevated filesystem access before treating Graphify as unavailable.
- Expected: graphify update . would create graphify-out from the writable course workspace.
- Actual: The first non-elevated Graphify update failed with [WinError 5], and the elevated retry succeeded with a 6327-node graph.
- Why: On this Windows managed workspace, Graphify output writes can hit filesystem permission boundaries even when normal repo files are writable.
- tags: graphify,windows,permissions

## 2026-08-09 -- After AD698 schedule/render verification, graphify update . can exceed 6 minutes; if workbook and serial Quarto renders pass, report Graphify as an incomplete maintenance step after confirming no graphify update process remains.
- Expected: Pinning the AD698 semester and rendering index.qmd, schedule.qmd, and deliverables.qmd would finish with a refreshed graphify-out graph.
- Actual: The generated Fall workbook and all three Quarto renders succeeded, but graphify update . timed out after 2 minutes and again after 6 minutes; elevated process checks showed no lingering Graphify process.
- Why: Graphify update is a repository-maintenance step whose runtime can exceed the task verification window, while schedule correctness is directly verified by data/fall26_generated_schedule.xlsx and rendered _site HTML date inspection.
- tags: graphify,schedule,verification,timeouts

## 2026-08-09 -- For AD698 Fall schedules, verify data/fall26_generated_schedule.xlsx has 12 Schedule rows, A1 has 12 on-campus dates, and O1 has six weekly online dates repeated in pairs before trusting index.qmd, schedule.qmd, or deliverables.qmd renders.
- Expected: Updating the AD698 pages to use the shared generated schedule would make Fall online and on-campus timelines match the course rule automatically.
- Actual: The pages used load_generated_schedule, but schedules/semester_planner.py still defaulted to 7 online weeks and 14 on-campus lectures, so O1 had seven single dates and A1 had fourteen rows until the planner expanded six weekly online dates into paired lecture rows and capped on-campus at 12.
- Why: The schedule count rule lives in schedules/semester_planner.py below the Quarto pages; page-level import checks do not prove the workbook has the right number of rows or repeated online dates.
- tags: schedule,calendar,online,oncampus,verification

## 2026-08-09 -- Before AD698 git add or commit recovery, if .git/index.lock blocks staging, run Get-Process git and inspect .git/index.lock Length and LastWriteTime; remove only a zero-byte stale lock when no git process exists.
- Expected: Staging and committing the selected schedule changes would proceed normally.
- Actual: git add failed because .git/index.lock already existed; no git process was running and the lock was zero bytes from August 6, 2026, so removing it allowed staging to continue.
- Why: A stale Git index lock in .git prevents all index writes until it is removed, but removing it is safe only after confirming no active git process owns it.
- tags: git,windows,stale-lock

## 2026-08-10 -- When AD698 full render fails in a Spark cell with Py4JError getConfs(ArrayList) does not exist, check the active Python with python -m pip show pyspark py4j and list pyspark/jars for mixed Spark versions before editing course content.
- Expected: The full Quarto render failure would point to a specific current .qmd source cell to fix.
- Actual: The pasted output failed while executing M05_P1.quarto_ipynb, but current M5/M05_P1.qmd has no executable Spark cell; the active system Python has pyspark 4.2.0 with both 4.1.1 and 4.2.0 Spark JARs installed.
- Why: Quarto can surface generated notebook names during render, and a dirty global PySpark install can make the Python API call JVM methods missing from older Spark JARs on the classpath.
- tags: quarto,pyspark,windows,verification

## 2026-08-10 -- For AD698 VS Code render tasks, remove generated *.quarto_ipynb* files before uv run quarto render --execute as well as after it; post-render-only cleanup can leave stale notebooks that surface old Spark/Py4J errors in the next full render.
- Expected: The Render and Zip Quarto Site task would execute current .qmd source files and then package _site.zip without stale notebook errors.
- Actual: The pasted full-render log executed an old M05_P1.quarto_ipynb Spark cell even though current M5/M05_P1.qmd renders cleanly and has no such executable Spark cell.
- Why: The .vscode/tasks.json cleanup ran only after a successful render, so any stale *.quarto_ipynb* files from an earlier run remained present at the start of the next render task.
- tags: quarto,vscode,cache,render-task,fix-applied

## 2026-09-17 -- Audit Reveal.js slide bodies separately from teaching notes and execute the displayed examples.
- In M1/M01_P2.qmd, instructor-facing rationale appeared as visible paragraphs, CBOW/Skip-gram explanations were duplicated, and the global echo: false setting hid instructional code. Use student-facing definitions, worked examples, and limitations; put any necessary presenter guidance in Quarto .notes blocks.
- Check formulas against the actual vectorizer options: smoothed scikit-learn IDF is log((1 + N)/(1 + df)) + 1, followed by normalization when norm="l2". In Python raw regex strings, use a single backslash in whitespace classes; verify with tabs and repeated spaces.
- The repository .venv lacks gensim on this machine while system Python has the slide dependencies. Check imports before choosing QUARTO_PYTHON for executable deck verification.
- tags: quarto,slides,academic-content,verification
- Verification outcome: all seven cells executed and the generated Reveal.js deck passed browser spot checks with no detected math errors or broken images. Quarto subsequently failed during website indexing because a project input requested the unavailable ad698-venv kernel; distinguish this project-index failure from slide execution or HTML generation.

## 2026-09-17 -- Use sibling-relative edustack wheel sources across Windows drives and regenerate the lockfile.
- AD698 depends on edustack-classroom and edustack-schedule (not edustack-calendar). With edustack beside this repository, use ../edustack/packages/<package>/dist/<wheel> in tool.uv.sources on either drive; each checkout must contain that package layout.
- Local version 0.1.1 wheels had different hashes from the old D: wheels. Run uv lock to record the actual artifacts, then uv lock --check --offline; changing only the paths leaves stale hashes. Offline regeneration requires cached registry metadata even when only local sources change.
- tags: uv,dependencies,windows,verification

## 2026-09-17 -- Match Quarto kernel names to installed Jupyter kernels, independently of the virtual environment name.
- M5/M05_P2.qmd requested ad698-venv, but the repository .venv exposes only python3. Changed the page to jupyter: python3, matching neighboring pages; Quarto inspection then resolved its kernel successfully.
- Creating or activating .venv does not register a kernel named ad698-venv. Inspect kernels with .venv/Scripts/python.exe -c "from jupyter_client.kernelspec import KernelSpecManager; print(KernelSpecManager().find_kernel_specs())". Set QUARTO_PYTHON to the resolved .venv/Scripts/python.exe path when explicitly selecting this environment; the unactivated shell otherwise selects system Python on this machine.
- tags: quarto,jupyter,venv,kernel,windows

## 2026-09-17 -- Verify a shared Reveal.js theme against every deck, including print layout.
- Apply presentation settings in each deck's revealjs format rather than the website HTML defaults. Explicit renders of excluded M7/M8 and help-code documents write HTML next to their sources; included modules write to _site.
- In print-pdf view, inspect .pdf-page heights against the configured 16:9 ratio, code scrollHeight versus clientHeight, missing image dimensions, and .katex-error elements. A double-height page identifies a slide that needs splitting or a different layout. Check normal slideshow screenshots too.
- Use a fresh preview query string after rebuilding: an existing browser URL served an older embedded-resource deck during the rollout. Confirm visible slide titles against the current source before accepting a layout audit.
- Dense nested lists fit comparison cards or columns; long code examples can be split at top-level statements. Compare the combined Python AST before and after reflow to verify that examples retain their behavior.
- A passing page-height check does not prove footer clearance or diagram-label legibility. Inspect dense slides in normal slideshow view; split formulas from their explanatory bullets when needed. Quarto's generated Mermaid SVG uses svg.mermaid-js, so a .mermaid svg selector alone can miss it. Use numbered cards for simple workflows whose SVG labels collide.
- Put a blank line before a new Markdown heading after display math; without it, Pandoc can keep the apparent heading inside the preceding list item. Set fig-height explicitly for shallow Graphviz pipelines to avoid a default 480-pixel canvas dominated by empty space.
- Check imports again before choosing a render interpreter. On this rollout, system Python had a pydantic/pydantic-core mismatch and lacked svgwrite; the project .venv imported gensim, spacy, and svgwrite successfully. Earlier environment observations are not permanent.
- tags: quarto,revealjs,theme,layout,verification,python
- Ignore `*.quarto_ipynb*`, including numbered suffixes; the narrower `*.quarto_ipynb` rule allowed eight temporary notebooks to be tracked. Keep the authored `.qmd` and intentional `.ipynb` files instead.

## 2026-09-17 -- For Reveal.js scrollbar fixes in AD698, remove advisory.scss overflow-x:auto overrides and verify both pre.sourceCode and .cell-output pre; code folding still requires code-fold:true in the deck YAML because SCSS cannot create details elements.
- Expected: The advisory theme would wrap long code and output lines without a horizontal scrollbar, with folding available from the presentation settings.
- Actual: advisory.scss had a later pre.sourceCode overflow-x:auto rule that reintroduced horizontal scrolling; M2/M02_P1.qmd also explicitly set code-fold:false.
- Why: CSS controls overflow and wrapping, while Quarto code folding is generated from document metadata; the two mechanisms are independent.
- tags: quarto,revealjs,theme,verification

## 2026-09-17 -- For AD698 HTML-theme verification on this Windows checkout, direct quarto render currently resolves Deno to a malformed D:/Repositories/AD698-generative-ai-for-BA/Files/Quarto/bin path, while uv run quarto is blocked when the sibling D:/Repositories/edustack wheel source is absent; compile theme SCSS with C:/Program Files/Quarto/bin/tools/x86_64/dart-sass/sass.bat and report page rendering as blocked until either environment issue is fixed.
- Expected: Representative Module 2 HTML pages would render after the metanalytics.scss update.
- Actual: Dart Sass compiled theme/metanalytics.scss successfully, but direct Quarto failed before rendering on a malformed Deno path and uv run failed before rendering because D:/Repositories/edustack was missing.
- Why: The installed Quarto and uv project execution paths depend on different local runtime assumptions; SCSS compilation is independent of Quarto page execution.
- tags: quarto,scss,windows,verification,environment

## 2026-09-20 -- For AD698 with EduStack 0.1.1, generate through schedules.generated_schedule: the generic CLI omits deliverables hooks. Verify exact A1 dates and nonempty deliverables sheets. Fall 2026 now has 14 Tuesday meetings from September 8 through December 15, superseding the older 12-meeting lesson; skip October 13 because it follows Monday's schedule.
- Expected: Package migration would preserve course dates and deliverables on the schedule and deliverables pages.
- Actual: The stored export had empty deliverables sheets and 12 Monday dates. The course wrapper now regenerates with deliverables, and all three pages rendered and passed HTML checks for their intended content.
- Why: The package loader only reads an export, the generic generator omits course hooks, and its substitution engine applies Monday dates to Tuesday sections. The source workbook also now has one section, so index.qmd's positional row deletion failed and was removed. Regression tests and HTML inspection cover these outcomes.
- tags: schedule,edustack,calendar,verification,fix-applied

## 2026-09-20 -- For AD698 render startup delays, time quarto inspect before changing caching: the 2026-09-20 checkout took 94.84 seconds versus 4.57 seconds for the same 117 inputs in a source-only copy.
- Expected: Separate notebook execution time from project startup overhead.
- Actual: help-code contained 100478 files and data contained 14675 files; source-only discovery was much faster. Full render timing was unavailable after a Sass subprocess Invalid handle error.
- Why: Quarto 1.11.1 expands recursive render include and exclude globs separately and also scans project YAML files; render exclusions do not eliminate all traversal. Compare effective input sets before attributing latency to caching. No configuration fix applied.
- tags: quarto,performance,discovery

## 2026-09-20 -- On this Windows managed checkout, schedule tests that write temporary .xlsx files can fail with PermissionError under the sandbox temp directory; rerun the same unittest command with elevated filesystem access before changing test or schedule code.
- Expected: python -m unittest tests/test_schedule_generation.py completes with 3 tests passing.
- Actual: The first run failed in two tests when pandas/openpyxl tried to create schedule.xlsx under the Windows Temp directory; the unchanged rerun with elevated access passed all 3 tests.
- Why: The sandbox denies pandas/openpyxl file creation and cleanup in its managed temporary directories, while the repository and test logic are valid.
- tags: tests,windows,permissions,schedule

## 2026-09-22 -- Extend the language guard with semantic-review findings, then distinguish source checks from render acceptance.
- Replacing the six originally reported violations exposed additional authoring commentary in M02_LN1, M02_LN2, M05_LN1, and M05_LN2. The checker now also detects classroom narrative, lecture-pause directions, teaching-activation claims, and teaching-oriented story-map rationale; regression examples exercise those phrases.
- `python scripts/check_course_language.py` and `python -m unittest discover -s tests -p test_course_language.py` verify source patterns and detector behavior only. They do not establish slide/notes coverage or rendered quality.
- The validation render of M2/M02_P1.qmd failed during project discovery at a missing M0/M0_T2_files/mediabag directory while other full-site and slide renders were active. Avoid adding another render against shared outputs during concurrent work; do not infer a source-content failure from that discovery error.
- tags: quarto,authoring-language,regression,concurrent-render,verification

## 2026-09-22 -- Audit PDF generation beyond Quarto front matter.
- The tokenization primer was the only document declaring a PDF output format, but utils/nn_diagrams.py and help-code/cuda_check.ipynb also invoked latexmk. Remove the compiler API, its package export, notebook invocation, and stale compilation outputs together. Keep reference PDF assets and subject-matter uses of PDF separate from generation.
- Parse document YAML and scan authored code, notebooks, and build configuration for PDF writers; checking only _quarto.yml misses per-document formats and helper commands.
- Quarto inspection during this change failed in project discovery on the missing M5/M05_LN1_files directory; source-format checks do not establish a successful site render.
- tags: quarto,pdf,build,verification
