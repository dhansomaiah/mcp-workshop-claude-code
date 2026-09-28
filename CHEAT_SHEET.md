# Cheat sheet

## Restart after editing `server.py`

Claude Code spawns `component-workshop` as a subprocess when the session starts — it does not pick up edits to `server.py` on its own. After you save an edit:

1. Exit Claude Code: `/exit` or Ctrl+D.
2. Run `claude` again.

This respawns the server and gives you a fresh conversation. Then re-ask your question.

## Claude Code doesn't see the `component-workshop` tools

- Run `/mcp` — it lists connected servers and their tools, plus an error log for any that failed to start.
- Make sure you started `claude` from the repo root. Claude Code looks for `.mcp.json` in the current directory, and `server.py` reads `data/` relative to its own location — if the server itself isn't launched from the repo root you'll get path errors (see below).
- Open `.mcp.json` — it should have an `mcpServers.component-workshop` block.
- If you declined the project's MCP-server trust prompt by mistake, run `claude mcp reset-project-choices` and restart `claude` to be asked again.

## Server won't start (error via `/mcp`)

Run `/mcp` and open the `component-workshop` entry to see its stderr. Usually one of:

- `ModuleNotFoundError: No module named 'mcp'` → run `pip install -r requirements.txt`
- `ModuleNotFoundError: No module named 'mcp.server.fastmcp'` → `mcp>=2.0` removed FastMCP; run `pip install --force-reinstall "mcp>=1.11,<2.0"`
- `FileNotFoundError: components.csv` → you weren't in the repo root when you ran `claude`. `cd` there and restart.
- Python syntax error → test the server alone in the terminal: `python server.py` (it should sit silently — stdio servers don't print). If you get a traceback, that's your bug.

## Tool doesn't appear after adding it

Almost always one of:

- Missing `@mcp.tool()` decorator (with parentheses) above the function.
- Forgot to exit and restart `claude` after saving.

## Tool call gets "Invalid arguments"

Parameter names in your function signature must match what Claude passes, case-sensitive. If your function is `def find_component_by_family(family: str)`, Claude passes `{"family": "..."}`.

## Claude keeps reading `data/components.csv` directly instead of calling the tool

Check that `.claude/settings.json` still has its `permissions.deny` block for `data/**`, and that you're in the same folder that file lives in (permission settings are per-project). If it's intact and Claude still bypasses your tool, explicitly tell it in the prompt to use its available tools instead of reading files.

## Editing in Codespaces

- File tree on the left. Save with `Ctrl+S`.

## Optional: the `python client.py` fallback

If Claude Code is having a bad day (network issue, MCP connection stuck), you can still exercise the MCP loop from the terminal:

```bash
python client.py
```

It does the handshake, lists tools, and calls `lookup_component("CM101A")` directly. No AI in the loop.
