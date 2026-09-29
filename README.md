# MCP Workshop

Build your first MCP server in 30 minutes.

**Prerequisites (before the workshop):** Python 3.10+ installed and on your PATH.

## What's inside

A tiny MCP server that serves synthetic embedded-flavored data — fake components (like `CM101A`) and fake NTC fault codes — plus a `.mcp.json` that hands it to **Claude Code** as a tool source. You'll add tools during the workshop and ask Claude to use them.

## Quick start (local clone, Windows)

1. Create a folder somewhere for the workshop (e.g. on your Desktop), open a terminal there, and clone this repo into it:
   ```
   git clone https://github.com/dhansomaiah/mcp-workshop-claude-code.git
   cd mcp-workshop-claude-code
   ```
   `git clone` creates its own `mcp-workshop-claude-code` subfolder — make sure you `cd` into it before continuing. Everything below assumes your terminal is inside that folder.
2. Run the setup script:
   ```
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```
   It checks Python is on PATH, then installs the Python dependencies.
3. Run:
   ```
   nxt-llm claude
   ```
   (Nexteer's standard launcher for Claude Code — routes through the internal AI gateway.) The first time you run it in this folder, Claude Code will ask to trust the project and to approve the `component-workshop` MCP server from `.mcp.json` — approve both.
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
- `setup.ps1` — one-time local setup (checks Python, installs dependencies)
- `HANDS_ON.md` — the two workshop tasks
- `CHEAT_SHEET.md` — restarts, common errors, troubleshooting
- `SOLUTION.md` — peek only if Claude stalls

## The mental model

An MCP server is a **toolbox with labeled drawers**. Each tool is a drawer. The tool's description string is the label taped on it. The AI reads the labels to decide which drawer to open.

**Your job as a tool author:** write labels the AI can act on.

## What you will build

See `HANDS_ON.md`.
