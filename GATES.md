# Gates: repository pull, reconciliation, targeted commits, and working tree cleanup

OWNS: GATES.md, LESSONS.md, help-code/Employability-rag/**, scripts/build_employability_rag.py, scripts/employability_rag_common.py, scripts/test_employability_rag.py, scripts/validate_employability_rag.py, .gitignore

Scope: Pull latest remote changes, make targeted commits for Employability RAG and lessons, clear working tree, stashes, redundant links, and ensure untracked section is completely empty.

- [x] G1: Remote changes pulled and local branch is fast-forwarded to include origin/main.
  CHECK: python -c "import subprocess; res = subprocess.run(['git', 'merge-base', '--is-ancestor', 'origin/main', 'HEAD']); assert res.returncode == 0; print('REMOTE_PULLED_AND_INTEGRATED')"
  EXPECT: REMOTE_PULLED_AND_INTEGRATED
  EVIDENCE: exit=0; shell=C:\WINDOWS\system32\cmd.exe; cwd=D:\Repositories\AD698-generative-ai-for-BA; path=e82e10f6254c/53 entries; output=REMOTE_PULLED_AND_INTEGRATED

- [x] G2: Employability RAG contract tests pass.
  CHECK: python scripts/test_employability_rag.py
  EXPECT: EMPLOYABILITY_RAG_CHECKS_PASSED
  EVIDENCE: exit=0; shell=C:\WINDOWS\system32\cmd.exe; cwd=D:\Repositories\AD698-generative-ai-for-BA; path=e82e10f6254c/53 entries; output=Ran 6 tests in 0.119s | OK

- [x] G3: Course language checks pass across repository.
  CHECK: python scripts/check_course_language.py
  EXPECT: PASS: known authoring-language patterns absent in 42 files.
  EVIDENCE: exit=0; shell=C:\WINDOWS\system32\cmd.exe; cwd=D:\Repositories\AD698-generative-ai-for-BA; path=e82e10f6254c/53 entries; output=PASS: known authoring-language patterns absent in 42 files. Semantic review, slide/notes parity, and rendered inspection still required.

- [x] G4: Text encoding check passes across repository.
  CHECK: python scripts/check_text_encoding.py
  EXPECT: 0 encoding issue(s).
  EVIDENCE: exit=0; shell=C:\WINDOWS\system32\cmd.exe; cwd=D:\Repositories\AD698-generative-ai-for-BA; path=e82e10f6254c/53 entries; output=PASS: 565 text files checked; 0 encoding issue(s).

- [x] G5: Untracked files list is empty, working tree is clean, and stash list is empty.
  CHECK: python -c "import subprocess; s = [l for l in subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines() if not l.endswith('GATES.md')]; st = subprocess.run(['git', 'stash', 'list'], capture_output=True, text=True).stdout.strip(); assert not s, f'Dirty tree: {s}'; assert not st, f'Stashes exist: {st}'; print('TREE_CLEAN_AND_EMPTY')"
  EXPECT: TREE_CLEAN_AND_EMPTY
  EVIDENCE: exit=0; shell=C:\WINDOWS\system32\cmd.exe; cwd=D:\Repositories\AD698-generative-ai-for-BA; path=e82e10f6254c/53 entries; output=TREE_CLEAN_AND_EMPTY
