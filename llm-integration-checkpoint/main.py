import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError


# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

# Stop if API key is missing
if not api_key:
    print("ERROR: OPENAI_API_KEY is missing.")
    print("Please create a .env file and add your API key.")
    sys.exit(1)


# Create the AI client
client = OpenAI(api_key=api_key)

# Small model suitable for learning tasks
MODEL = "gpt-5-mini"

# System instructions for the assistant
SYSTEM_PROMPT = """
You are a helpful learning assistant.

Explain concepts clearly and simply, especially for beginners.
Use examples when they make the explanation easier to understand.
Break difficult topics into smaller steps.
Do not invent facts or make up information.
If you are unsure about something, clearly say that you are unsure
rather than presenting an unverified answer as fact.
"""


def ask_assistant(question):
    """Send a question to the AI model and return the response."""

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=question
    )

    answer = response.output_text

    # Get token usage when available
    usage = response.usage

    if usage:
        input_tokens = getattr(usage, "input_tokens", "N/A")
        output_tokens = getattr(usage, "output_tokens", "N/A")
        total_tokens = getattr(usage, "total_tokens", "N/A")
    else:
        input_tokens = output_tokens = total_tokens = "N/A"

    return answer, input_tokens, output_tokens, total_tokens


def main():
    print("=" * 50)
    print("        AI LEARNING ASSISTANT")
    print("=" * 50)
    print(f"Model: {MODEL}")
    print("Type 'exit' or 'quit' to close the program.")
    print()

    while True:
        question = input("You: ").strip()

        # Ignore empty questions
        if not question:
            print("Please enter a question.")
            continue

        # Exit commands
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            answer, input_tokens, output_tokens, total_tokens = (
                ask_assistant(question)
            )

            print("\nAssistant:")
            print(answer)

            print("\n--- Usage ---")
            print(f"Model: {MODEL}")
            print(f"Input tokens: {input_tokens}")
            print(f"Output tokens: {output_tokens}")
            print(f"Total tokens: {total_tokens}")
            print()

        except AuthenticationError:
            print("\nERROR: Authentication failed.")
            print("Please check that your OPENAI_API_KEY is correct.\n")

        except RateLimitError:
            print("\nERROR: Rate limit reached.")
            print("Please wait a moment and try again.\n")

        except Exception as error:
            print("\nERROR: Something unexpected happened.")
            print(f"Details: {error}\n")


if __name__ == "__main__":
    main()

