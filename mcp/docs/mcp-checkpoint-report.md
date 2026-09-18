# MCP Checkpoint Report

## 1. MCP Architecture

The project uses a simple MCP client-server architecture with Gemini as the AI model.

```text
User
  |
  v
Gemini Agent
  |
  | Selects tool and generates arguments
  v
MCP Client
  |
  | stdio
  v
MCP Server
  |
  +--> explain_topic
  |
  +--> create_study_plan
  |
  +--> generate_revision_checklist
  |
  +--> study://overview
```

The MCP server is started as a separate Python process. The client connects to it using the `stdio` transport. The client first calls `list_tools()` to discover the available tools and their input schemas. These tool definitions are then provided to Gemini as function declarations.

Gemini can select an appropriate tool and generate the required arguments. The client then sends the tool call to the MCP server using `session.call_tool()`.

## 2. Available Tools

### `explain_topic`

This tool provides a simple explanation of a requested topic.

Example input:

```json
{
  "topic": "MCP",
  "level": "beginner"
}
```

### `create_study_plan`

This tool creates a study plan for a topic.

Example input:

```json
{
  "topic": "MCP",
  "days": 3,
  "hours_per_day": 2
}
```

### `generate_revision_checklist`

This tool generates a revision checklist from a list of topics.

Example input:

```json
{
  "topic": "MCP",
  "topics": ["MCP architecture", "MCP tools", "MCP resources"]
}
```

## 3. MCP Resource

The server exposes the following resource:

```text
study://overview
```

The resource provides a short description of the study tools available through the MCP server.

Example response:

```text
This MCP server provides tools for explaining topics,
creating study plans, and generating revision checklists.
```

## 4. Client Test

The client was tested with the following request:

```text
Create a 3-day plan to learn MCP.
```

The MCP client first discovered the available tools:

```text
Available MCP tools:
- explain_topic
- create_study_plan
- generate_revision_checklist
```

Gemini selected the `create_study_plan` tool and generated arguments similar to:

```text
Gemini selected tool:
create_study_plan

Arguments:
{
    "topic": "MCP",
    "days": 3
}
```

The client then passed the tool call to the MCP server.

Example result:

```text
Tool result:
{
  "topic": "MCP",
  "days": 3,
  "hours_per_day": 2,
  "plan": [
    {
      "day": 1,
      "topic": "MCP",
      "hours": 2,
      "task": "Study MCP - Day 1"
    },
    {
      "day": 2,
      "topic": "MCP",
      "hours": 2,
      "task": "Study MCP - Day 2"
    },
    {
      "day": 3,
      "topic": "MCP",
      "hours": 2,
      "task": "Study MCP - Day 3"
    }
  ]
}
```

This test confirmed that the client could discover the MCP tools, provide them to Gemini, receive a function call, and execute the selected tool through the MCP server.

## 5. Tool Failure Test

One tool failure was tested by providing invalid input to `create_study_plan`.

For example, the client attempted to call the tool without the required `topic` argument:

```json
{
  "days": 3
}
```

The server/tool rejected the request because `topic` is a required parameter.

The client reported the failure instead of executing the tool with incomplete data:

```text
Agent workflow failed:
create_study_plan requires a topic.
```

This shows that invalid tool arguments can be detected before the tool is executed.

Another example would be passing an invalid value for `days`:

```json
{
  "topic": "MCP",
  "days": "three"
}
```

Since `days` should be an integer, this request should also be rejected.

## 6. Security

The MCP client does not automatically execute arbitrary functions returned by the model. The selected tool name should be checked against the tools discovered from the MCP server.

For example:

```python
if tool_name not in allowed_tools:
    raise ValueError(
        f"Gemini selected an unknown tool: {tool_name}"
    )
```

This prevents the model from requesting a tool that is not exposed by the MCP server.

The application also relies on the MCP tool schemas to define the expected input parameters. This helps reduce invalid tool calls.

The server currently uses `stdio` transport, which means the MCP server runs as a local process started by the client. This is useful for development and testing because the server is not exposed as a public network service.

API keys such as the Gemini API key are loaded from environment variables rather than being hard-coded in the source code:

```python
client = genai.Client(
    api_key=os._
```
