# Task 6: conversation with Claude Code about spawning subagents

Me: We still have some excersices or rather tasks left in week 8, I want you to run as much subagents as there is tasks left to do and each agent to summarize what is there to be done in that task simply and shortly in 1-2 sentences, run cheaper models for subagents for examle Sonnet ones.

Claude asked, I answered:
- Which Week 08 tasks count as "left to do", so I spawn one subagent for each? → Tasks 7, 8, 9 and Bonus 10. Everything after the task we're doing now: 4 subagents.
- Which cheaper model should the subagents run on? I (the orchestrator) stay on Opus. → Sonnet
- Should I set the subagent up as a reusable config file, or just spawn it once? → Create .claude/agents/task-summarizer.md with the model, read-only tools and a 1-2 sentence limit. It shows up in /agents and can be reused.

## Subagent results

Claude created `.claude/agents/task-summarizer.md` (model: sonnet, tools: Read) and ran 4 Sonnet subagents in parallel, one per task. Their answers:

Task 7: The task asks you to create a simple local MCP server with one simple MCP tool, then make your coding assistant call that tool once to show it works. You hand in the files that make up the server and tool.

Task 8: The task asks you to create a simple rule in the repository (for example, "whenever you generate a new file, include which agent and model created it") and check that your coding assistant follows it. The OUTPUT is the rule file, placed properly in the repo, plus the conversation showing the assistant respected it.

Task 9: The task asks you to find the file(s) where your coding assistant saved the settings changes made in earlier tasks, and to submit it with the API key and any other sensitive data censored, so that it matches your screenshots.

Bonus Task 10: The task is an optional bonus (1.0b) that asks you to describe your typical workflow with LLM tools: web chat, coding assistants, copy-pasting between tools, spawning subagents, and so on. The OUTPUT is a short report plus a figure showing the steps, validation loops and components in that workflow.
