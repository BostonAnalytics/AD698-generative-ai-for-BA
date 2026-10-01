# Gates: repository cleanup

OWNS: GATES.md, README.md, LESSONS.md, .gitignore, .vscode/tasks.json, copilot-instructions.md, requirements.txt, help-code/maintenance/README.md, tracked runtime caches, temporary .vdoc exports, _module_qmd_files.txt, output.txt

Scope: synchronize branches, review and clear the stash, remove obsolete runtime artifacts and documentation, make targeted commits, and push a clean checkout.

- [x] G1: Remote branches fetched and local tracking branches synchronized without discarding unique commits.
  EVIDENCE: PowerShell at repository root: git fetch --all --prune and git merge --ff-only origin/main exited 0; main advanced d451318 to f8726a7. Spring2026...origin/Spring2026 measured 0/0; main..Summer2026 measured 0 commits. gh-pages fetched as deployment output, not merged into source.
- [x] G2: Stash reviewed and cleared with any unique work recoverable.
  EVIDENCE: April stash b640a6ae6e14583b10e60b6259e7dfbb4f3aee78 reviewed against its base and current source. September commit 2dc9e67 already reconciles stashed course updates. git bundle verify .git/pre-cleanup-stash-20261001.bundle exited 0 and confirmed complete history; git stash drop exited 0; git stash list is empty. The bundle remains local and is not pushed.
- [x] G3: Tracked runtime caches removed and obsolete setup documentation reconciled with current configuration.
  EVIDENCE: Removed 250 Jupyter-cache files, 26 bytecode files, 9 R-session files, 22 editor exports, and 2 machine-specific inventory outputs. Removed obsolete requirements.txt snapshot; pyproject.toml and uv.lock remain authoritative. Updated empty README, stale Copilot instructions, task schema version, and machine-specific maintenance link. No separate plans/phases/tasks documents, tracked symlinks/shortcuts, or app entry points were found. Existing course/project milestone content and historical references retained.
- [x] G4: Focused validation passes and final diff contains only intended cleanup.
  EVIDENCE: PowerShell at repository root: language guard passed across 42 files; all 4 language regression tests passed; git diff --check exited 0. Python checks passed for edited Markdown links, JSON task version 2.0.0, TOML parsing, and absence of removed artifact classes. git check-ignore positively matched all seven cache/environment probes. Diff reviewed; no authored course source changed. Graphify update exited 0 with 6064 nodes and 6687 edges; generated index retained locally and ignored. Full course render, notebook execution, and slide/notes parity were not rerun for this maintenance-only change.
- [ ] G5: Targeted commits pushed; working tree, untracked list, and stash list empty.
  EVIDENCE: pending
