# Where the Week 08 configuration lives

The slash command (Task 2, `.claude/commands/next.md`), the output style I use as a profile (Task 4, `.claude/output-styles/lab-tutor.md`) and the skill (Task 5, `.claude/skills/explain-concept/SKILL.md`) and the subagent (Task 6, `.claude/agents/task-summarizer.md`) are all in the `.claude/` folder in the repository root, and `AGENTS.md` (Task 3) is in the root itself. The MCP server from Task 7 is registered in `.mcp.json` in the root, and its code is `Week_08_Dissecting/task7_mcp_server.py`.

Anything new of the same kind goes to the matching place: slash commands to `.claude/commands/<name>.md`, output styles to `.claude/output-styles/<name>.md`, skills to `.claude/skills/<name>/SKILL.md` subagents to `.claude/agents/<name>.md`, rules (Task 8) to `.claude/rules/<name>.md` and MCP servers to `.mcp.json`. The task outputs themselves (screenshots, explanations, conversation records) are in `Week_08_Dissecting/` with a `taskN_` prefix.
