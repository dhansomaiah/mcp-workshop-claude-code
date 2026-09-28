# MCP Workshop

Build your first MCP server in 30 minutes.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/dhansomaiah/mcp-workshop-claude-code)

## What's inside

A tiny MCP server that serves synthetic embedded-flavored data — fake components (like `CM101A`) and fake NTC fault codes — plus a `.mcp.json` that hands it to **Claude Code** as a tool source. You'll add tools during the workshop and ask Claude to use them.

## Quick start (in Codespaces)

1. Click **Open in Codespaces** above.
2. Wait ~90 seconds for the environment to build (`pip install` and the Claude Code CLI install run automatically).
3. Open a terminal and run:
   ```
   claude
   ```
   The first time you run it in this folder, Claude Code will ask to trust the project and to approve the `component-workshop` MCP server from `.mcp.json` — approve both.
4. Run `/mcp` — you should see `component-workshop` connected with two tools.
5. Ask Claude:
   > **who owns component CM101A?**

   Claude picks `lookup_component`, calls it (approve the tool call if you're prompted), and answers.

That's the whole loop. The workshop tasks are edits to it — see `HANDS_ON.md`.

## What's here

- `server.py` — the MCP server, two working tools
- `.mcp.json` — registers the server with Claude Code
- `.claude/settings.json` — blocks Claude's built-in file tools from reading `data/` directly, so it's forced to go through your MCP tools instead of just opening the CSV
- `data/` — synthetic components and NTCs
- `client.py` — optional stdio client, prints raw wire messages (no AI)
- `HANDS_ON.md` — the two workshop tasks
- `CHEAT_SHEET.md` — restarts, common errors, troubleshooting
- `SOLUTION.md` — peek only if Claude stalls

## The mental model

An MCP server is a **toolbox with labeled drawers**. Each tool is a drawer. The tool's description string is the label taped on it. The AI reads the labels to decide which drawer to open.

**Your job as a tool author:** write labels the AI can act on.

## What you will build

See `HANDS_ON.md`.
