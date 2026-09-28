"""
MCP server for the workshop.

Serves synthetic embedded-flavored data:
  - lookup_component: find a component by ID
  - list_ntcs_for_component: list NTCs handled by a component

Run:  python server.py
"""
from pathlib import Path
import csv
import json

from mcp.server.fastmcp import FastMCP

DATA_DIR = Path(__file__).parent / "data"

mcp = FastMCP("component-workshop")


def _load_components() -> list[dict]:
    with open(DATA_DIR / "components.csv", newline="") as f:
        return list(csv.DictReader(f))


def _load_ntcs() -> dict:
    with open(DATA_DIR / "ntcs.json") as f:
        return json.load(f)


@mcp.tool()
def lookup_component(component_id: str) -> dict:
    """Look up a component by its ID (e.g. CM101A, ES249B, AR200A).

    Returns the component's functional name, owner, family, and subsystem.
    Use this when the user asks who owns a component, what family it belongs
    to, or wants basic component metadata.
    """
    for row in _load_components():
        if row["id"].lower() == component_id.lower():
            return row
    return {"error": f"No component found with ID '{component_id}'"}


@mcp.tool()
def list_ntcs_for_component(component_id: str) -> list:
    """List all NTCs (fault codes) handled by a given component.

    Returns each NTC with its number, type, priority, and short description.
    Use this when the user asks what faults a component detects, or what NTCs
    a component owns.
    """
    ntcs = _load_ntcs()
    return ntcs.get(component_id.upper(), [])


if __name__ == "__main__":
    mcp.run()
