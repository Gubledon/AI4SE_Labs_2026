# Date and time in report file names

Whenever you create a new report or other Markdown file in this repo, add the current date and time to the end of its file name in the form `_YYYY-MM-DD_HH-MM`, for example `task8_report_2026-11-22_14-35.md`.

- Get the real local time by running `date +%Y-%m-%d_%H-%M` right before creating the file. Don't guess it.
- Use hyphens in the time, not colons (colons aren't allowed in Windows file names).
- This applies only to new files. Don't rename existing files, and don't apply it to configuration files (`CLAUDE.md`, `AGENTS.md`, `SKILL.md`, files in `.claude/`) or to code.
