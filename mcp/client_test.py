import asyncio
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


async def main():

    user_request = "Create a simple study plan for a subject: python variables, for 3 days, 3 hours"

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )

    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()
            
            # 1. Get tools from MCP
            tools_response = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools_response.tools:
                print(f"- {tool.name}")

            allowed_tools = {
                tool.name: tool
                for tool in tools_response.tools
            }

            
            # 2. Convert MCP tools to Gemini tools
            function_declarations = []

            for tool in tools_response.tools:

                function_declarations.append(
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description or "",
                        parameters_json_schema=tool.input_schema
                    )
                )

            gemini_tool = types.Tool(
                function_declarations=function_declarations
            )

            
            # 3. Ask Gemini to choose a tool
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_request,
                config=types.GenerateContentConfig(
                    tools=[gemini_tool],
                    temperature=0
                )
            )

            
            # 4. Check Gemini's response
            if not response.candidates:
                raise ValueError(
                    "Gemini returned no candidates."
                )

            candidate = response.candidates[0]

            if not candidate.content:
                raise ValueError(
                    "Gemini returned no content."
                )

            
            # 5. Check for function calls
            function_calls = []

            for part in candidate.content.parts:

                if part.function_call:
                    function_calls.append(
                        part.function_call
                    )

            if not function_calls:

                print("\nGemini response:")

                if response.text:
                    print(response.text)
                else:
                    print("Gemini did not request a tool.")

                return

            
            # 6. Execute Gemini's selected MCP tool
            for function_call in function_calls:

                tool_name = function_call.name

                arguments = function_call.args or {}

                print("\nGemini selected tool:")
                print(tool_name)

                print("\nArguments:")
                print(arguments)

                
                # Safety check
                if tool_name not in allowed_tools:
                    raise ValueError(
                        f"Gemini selected an unknown tool: {tool_name}"
                    )

                
                # Execute MCP tool
                result = await session.call_tool(
                    tool_name,
                    arguments
                )

                print("\nTool result:")

                for content in result.content:

                    if hasattr(content, "text"):
                        print(content.text)
                    else:
                        print(content)


if __name__ == "__main__":
    asyncio.run(main())