"""
Minimal MCP client for the workshop.

Spawns server.py, does the handshake, lists the tools it exposes,
calls one, and prints the result.

Run:  python client.py

If you're wondering what "the wire" looks like, this file is it.
"""
import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    # Tell the client HOW to launch our server.
    # stdio transport: parent and child talk over stdin/stdout.
    server = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            # ---- 1. Handshake --------------------------------------------
            await session.initialize()
            print("[handshake] connected to server\n")

            # ---- 2. list_tools --  which drawers exist? -----------------
            tools = await session.list_tools()
            print("[list_tools] drawers available:")
            for tool in tools.tools:
                first_line = (tool.description or "").splitlines()[0]
                print(f"  - {tool.name}: {first_line}")
            print()

            # ---- 3. call_tool --  open a drawer -------------------------
            print("[call_tool] lookup_component(component_id='CM101A')")
            result = await session.call_tool(
                "lookup_component",
                {"component_id": "CM101A"},
            )
            for block in result.content:
                text = getattr(block, "text", str(block))
                try:
                    print(json.dumps(json.loads(text), indent=2))
                except Exception:
                    print(text)


if __name__ == "__main__":
    asyncio.run(main())
