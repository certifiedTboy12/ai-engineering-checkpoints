import math
import ollama


MODEL = "llama3.1:8b"


# Tool 1: Calculator
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:
        allowed = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
        }

        result = eval(
            expression,
            {"__builtins__": {}},
            allowed
        )

        return str(result)

    except Exception as error:
        raise ValueError(f"Calculator error: {error}")


# Tool 2: Search
def search(query: str) -> str:
    """Search for information."""

    # Simulate a search failure
    if "404" in query.lower():
        raise TimeoutError("Search tool failed.")

    results = {
        "tunisia": (
            "Tunisia is a country in North Africa. "
            "Its capital is Tunis."
        ),

        "python": (
            "Python is a programming language commonly "
            "used for web development, automation, data science, and AI."
        )
    }

    query_lower = query.lower()

    for keyword, result in results.items():
        if keyword in query_lower:
            return result

    return f"No useful search result was found for: {query}"

# Give the functions to Ollama
tools = [
    calculator,
    search
]

# Agent
def agent(user_input: str):

    messages = [
        {
            "role": "system",
            "content": """
You are a helpful AI agent.

You have access to two tools:

1. calculator - Use this for mathematical calculations.
2. search - Use this when external information is needed.

Decide yourself whether a tool is necessary.

If the question can be answered directly, do not use a tool.
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # First call: let the LLM decide whether to use a tool
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    # Add the LLM response to the conversation
    messages.append(response["message"])

    # Check if the LLM requested tools
    if not response["message"].get("tool_calls"):

        print("Source: Direct Ollama LLM")

        return response["message"]["content"]

    # Execute requested tools
    for tool_call in response["message"]["tool_calls"]:

        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]

        print(f"LLM selected tool: {function_name}")

        try:

            if function_name == "calculator":

                result = calculator(
                    arguments["expression"]
                )

            elif function_name == "search":

                result = search(
                    arguments["query"]
                )

            else:

                result = "Unknown tool."

            print(f"Tool result: {result}")

            # Send the tool result back to Ollama
            messages.append(
                {
                    "role": "tool",
                    "content": result
                }
            )

        except Exception as error:

    
            # Tool failed → fallback to LLM
            print(f"Tool failed: {error}")
            print("Source: Ollama LLM fallback")

            messages.append(
                {
                    "role": "tool",
                    "content": (
                        f"The tool failed with this error: {error}. "
                        "Answer the user's question directly "
                        "without using the failed tool."
                    )
                }
            )

    # Final LLM response
    final_response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    print("Source: Ollama after tool execution")

    return final_response["message"]["content"]


# TESTS
print("TEST 1")

question = "What is sqrt(144) + 5?"

print("User:", question)
print("Agent:", agent(question))



print("TEST 2")

question = "Search 404 test"

print("User:", question)
print("Agent:", agent(question))


print("TEST 3")
question = "Who are you?"

print("User:", question)
print("Agent:", agent(question))



print("TEST 4")
question = "Tell me something about Tunisia"

print("User:", question)
print("Agent:", agent(question))