# Task 1: Cloning AI4SE_Playground

I asked Claude Code to clone the repository. The model itself can't touch the network or the disk. Claude Code gives it a Bash tool: the model writes a shell command, Claude Code runs it in my terminal and returns the output. So the clone was done by the normal `git` on my machine:

```
git clone https://github.com/Neltharion59/AI4SE_Playground.git
rm -rf AI4SE_Playground/.git
```

The repo is public, so no credentials were needed. Deleting `.git` keeps it from being a nested repository inside mine.
