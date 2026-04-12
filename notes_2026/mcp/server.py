from random import randint, choice
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp_demo")


@mcp.tool()
def d6() -> int:
    """Returns random number 1 - 6"""
    return randint(1, 6)


@mcp.tool()
def random_item(items: list[str]) -> str:
    """Returns random item from list of elements"""
    return choice(items)


if __name__ == "__main__":
    mcp.run(transport="sse")
