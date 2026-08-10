# Lessons

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
