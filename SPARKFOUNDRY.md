# Build a Spark Foundry course ZIP

Run from this course repository. The YAML selects and orders M1–M6 (12 lectures), excluding M0. AD698 also excludes M7–M8, matching its current Quarto website. Change the YAML if you want a different selection; keep lecture IDs stable.

Check that every selected source exists:

```powershell
uv run --with pyyaml python sparkfoundry_pack.py check
```

Render the selected notes, Reveal.js presentations and labs, then create the upload ZIP:

```powershell
uv run --with pyyaml python sparkfoundry_pack.py build --render
```

This runs Quarto serially with the course repository's existing pre-render hooks and execution settings. It can execute notebook cells, use configured APIs and take time. It does not start a server. Rendering occurs in `_sparkfoundry/rendered/`; the finished ZIP is `_sparkfoundry/<course-code>-<version>.zip`. Images and presentation resources are embedded in the HTML. The ZIP contains only selected HTML, original QMD sources, and manifests, not your datasets, credentials, solutions, or whole repository.

After a successful render, you can recreate the ZIP without rendering again:

```powershell
uv run --with pyyaml python sparkfoundry_pack.py build
```

The command checks source, render and format fingerprints. Changed sources or missing renders require `build --render`. Theme or dependency changes also require a fresh render. QMD downloads remain original source files and require the course repository's supporting files/environment to execute.

In Spark Foundry, sign in with staff course-editing permissions. On the learning home page, choose **Upload a course**, select the ZIP, inspect the draft outline and preview links, then select **Publish course**. The new course appears without rebuilding the frontend. This requires deployment of the upload feature first.

Increase `course.version` in `sparkfoundry.yml` for each changed publication. Re-uploading an identical ZIP is idempotent; changing an existing version is rejected. Old course versions, enrollments, progress and submissions are retained. Completion is not automatically granted for revised content. Stable lecture IDs retain identity and browser bookmarks.

The packager is a portable copy of `scripts/sparkfoundry_pack.py` from met-employability-services. Update both repository copies when updating the package format. The ZIP validation command is:

```powershell
uv run --with pyyaml python sparkfoundry_pack.py validate --zip _sparkfoundry/your-course-version.zip
```
