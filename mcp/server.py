# from mcp.server.fastmcp import FastMCP  

# mcp = FastMCP("project-tools")

# @mcp.tool()
# def add_numbers(a: int, b: int) -> dict:
#     """Add two numbers and return the result."""
#     return {
#         "a": a,
#         "b": b,
#         "result": a + b
#     }

# @mcp.resource("project://overview")
# def project_overview() -> str:
#     """Return a short description of the current project."""
#     return "This project exposes safe tools and resources through MCP."

# if __name__ == "__main__":
#     mcp.run(transport="stdio")

# from mcp.server.mcpserver import MCPServer

# mcp = MCPServer("project-tools")


# @mcp.tool()
# def add_numbers(a: int, b: int) -> dict:
#     """Add two numbers and return the result."""
#     return {
#         "a": a,
#         "b": b,
#         "result": a + b
#     }

# @mcp.resource("project://overview")
# def project_overview() -> str:
#     """Return a short description of the current project."""
#     return "This project exposes safe tools and resources through MCP."


# if __name__ == "__main__":
#     mcp.run(transport="stdio")


from mcp.server.mcpserver import MCPServer

mcp = MCPServer("study-tools")


@mcp.tool()
def explain_topic(topic: str, level: str = "beginner") -> dict[str, object]:
    """Provide a simple explanation of a study topic."""
    return {
        "topic": topic,
        "level": level,
        "explanation": (
            f"{topic} is an important topic that can be understood "
            f"by learning its main concepts, how they work, and "
            f"how they are applied in practice."
        )
    }


@mcp.tool()
def create_study_plan(
    subject: str,
    duration_days: int,
    hours_per_day: float = 2
) -> dict[str, object]:
    """Create a simple study plan for a subject."""
    return {
        "subject": subject,
        "duration_days": duration_days,
        "hours_per_day": hours_per_day,
        "plan": [
            {
                "day": day,
                "task": f"Study {subject} - Day {day}"
            }
            for day in range(1, duration_days + 1)
        ]
    }


@mcp.tool()
def generate_revision_checklist(
    subject: str,
    topics: list[str]
) -> dict[str, object]:
    """Generate a revision checklist for a subject."""
    return {
        "subject": subject,
        "checklist": [
            {
                "topic": topic,
                "completed": False
            }
            for topic in topics
        ]
    }


@mcp.resource("study://overview")
def study_overview() -> str:
    """Return a description of the study tools available through MCP."""
    return (
        "This MCP server provides tools for explaining topics, "
        "creating study plans, and generating revision checklists."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")