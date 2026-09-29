# Hands-on tasks

## Warm-up (~2 min) — make sure Claude Code sees our server

1. Open a terminal at the repo root (after running `setup.ps1` — see `README.md` if you haven't).
2. Run `nxt-llm claude`. First time only: approve the folder trust prompt and the `component-workshop` MCP server prompt.
3. Run `/mcp` — you should see `component-workshop` listed with two tools. (This repo's `.claude/settings.json` blocks Claude's built-in file tools from reading `data/` directly — same idea as Copilot's "uncheck every tool except component-workshop," just enforced as a project setting instead of a per-session click.)
4. Ask Claude:
   > **who owns component CM101A?**

   Expected: Claude calls `lookup_component` (approve the tool call if prompted) and answers with something like *"CM101A (MotAgCorrln) is owned by Dave Smith, Motor Control family, EPS subsystem."*

That's the entire loop. The two tasks below are small edits to it.

---

## Task 1 — Relabel the drawer (~5 min)

Every tool advertises itself to the AI through **three** things: its **name**, its **description**, and its **parameters**. Claude reads all three to decide which tool to call. Change any one badly and Claude may pick a different tool — or none at all.

Open `server.py`. Fully repurpose `lookup_component` so it *looks* like an HR tool — every part of the signature:

**Before:**
```python
@mcp.tool()
def lookup_component(component_id: str) -> dict:
    """Look up a component by its ID (e.g. CM101A, ES249B, AR200A).

    Returns the component's functional name, owner, family, and subsystem.
    Use this when the user asks who owns a component ...
    """
    for row in _load_components():
        if row["id"].lower() == component_id.lower():
            return row
    return {"error": f"No component found with ID '{component_id}'"}
```

**After — rename the function, the parameter, and rewrite the docstring:**
```python
@mcp.tool()
def fetch_hr_record(badge_number: str) -> dict:
    """Fetch employee HR records by their badge number."""
    for row in _load_components():
        if row["id"].lower() == badge_number.lower():
            return row
    return {"error": f"No employee found with badge '{badge_number}'"}
```

Three changes: **function name**, **parameter name**, **docstring**. Body is otherwise unchanged — the tool still works internally, it's just fully **misadvertised**.

> If you only change the docstring, Claude notices the parameter is still called `component_id` and figures out the real purpose. You have to lie *consistently* — that's the lesson.

Save. Then reload without leaving Claude Code:
1. Run `/mcp`, select `component-workshop`, choose **Reconnect** — this respawns the subprocess so it picks up your edit.
2. Run `/clear` — wipes conversation memory. Skip this and Claude may just cite its *previous* answer from memory instead of genuinely losing the tool, which muddies the lesson.

Ask:
> **who owns component CM101A?**

Claude has no tool that looks relevant. It backs off ("I don't have a tool for that"), tries to answer without one, or reaches for a wrong tool.

Revert the changes. Save. `/mcp` → Reconnect → `/clear`. Ask again. Original answer returns.

**Lesson:** the whole signature is the interface — **name, description, parameters, all three**. Claude picks tools by reading them together. Get any one badly wrong and your tool becomes invisible.

---

## Task 2 — Build a new drawer (~10 min)

Add a new tool to `server.py` called `find_component_by_family`. It should take a family name (`"Motor Control"`, `"Sensors"`, `"Arbitration"`, ...) and return every component in that family.

**What the data looks like** (from `data/components.csv`, loaded by `_load_components()` at the top of `server.py`):

```python
_load_components()  # returns a list of dicts, one per row:
[
    {"id": "CM101A", "name": "MotAgCorrln",   "owner": "Dave Smith",     "family": "Motor Control", "subsystem": "EPS"},
    {"id": "ES249A", "name": "HwTqEstm",      "owner": "Bob Brown",      "family": "Sensors",       "subsystem": "EPS"},
    {"id": "AR200A", "name": "FordHwAgArbn",  "owner": "John Davis",     "family": "Arbitration",   "subsystem": "EPS"},
    # ...20 rows total
]
```

Available `family` values in the data: **Motor Control**, **Sensors**, **Arbitration**, **Diagnostics**, **Communication**, **Power**, **Safety**.

You can open `data/components.csv` in the editor at any time to peek at all 20 rows.

Claude will do most of the typing:

```python
@mcp.tool()
def find_component_by_family(family: str) -> list:
    """<< write a description Claude can act on >>"""
    # << your code — filter _load_components() by family >>
```

Save. Run `/mcp`, select `component-workshop`, choose **Reconnect** so the server picks up the new tool (no need for `/clear` here — memory doesn't matter for this task). `/mcp` again to confirm you now see three tools.

Ask:
> **which components are in the Sensors family?**

Claude should call your new tool and answer with `HwTqEstm`, `HwTqArbn`, `TorqRateLmt`.

**Bonus if you finish early:** add one more tool that combines the two — given a family name, return every component AND its NTCs. Then ask:
> **what faults does the Sensors family cover?**

---

## Peek under the hood (optional)

Curious what a tool call actually looks like on the wire, without any AI in the loop? Run:

```bash
python client.py
```

That is a minimal stdio client: handshake → `list_tools` → `call_tool("lookup_component", "CM101A")` → prints the raw JSON. It is the same signal-trace flow you saw on the slides, in ~40 lines.

---

## Two rules to remember across both tasks

1. **After every `server.py` edit: `/mcp` → select `component-workshop` → Reconnect.** This respawns the server subprocess so your change takes effect — no need to exit Claude Code or relaunch `nxt-llm claude`.
2. **Follow Reconnect with `/clear` whenever memory could let Claude cheat** (Task 1's "does the tool still work" test). Skip it when memory doesn't matter (Task 2).
3. **Don't remove `.claude/settings.json`.** It's what stops Claude from bypassing your tool entirely and reading `data/` directly.
