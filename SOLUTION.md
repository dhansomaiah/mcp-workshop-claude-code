# Solutions — peek only if Claude stalls

## Task 2 — `find_component_by_family`

```python
@mcp.tool()
def find_component_by_family(family: str) -> list:
    """List all components belonging to a given family
    (e.g. 'Motor Control', 'Sensors', 'Arbitration', 'Diagnostics').

    Returns each component's id, name, owner, and subsystem.
    Use this when the user asks which components handle a functional area
    or belong to a subsystem group.
    """
    return [
        row for row in _load_components()
        if row["family"].lower() == family.lower()
    ]
```

## Bonus — `components_and_ntcs_by_family`

```python
@mcp.tool()
def components_and_ntcs_by_family(family: str) -> list:
    """List every component in a family along with the NTCs it handles.

    Use this when the user wants a full picture of a subsystem's fault
    coverage — e.g. 'what faults does the Sensors family detect?'
    """
    ntcs = _load_ntcs()
    return [
        {**row, "ntcs": ntcs.get(row["id"], [])}
        for row in _load_components()
        if row["family"].lower() == family.lower()
    ]
```
