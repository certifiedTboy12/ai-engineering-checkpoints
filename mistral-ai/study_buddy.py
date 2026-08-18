import os
import sys
import asyncio
from dotenv import load_dotenv
from typing import List, Optional
from mistralai.client import Mistral

load_dotenv()

class StudyBuddy:
    
    def __init__(self):
        self.conversations: List[dict[str, str]] = []
        self.topic_sumarry: Optional[str] = None
        self.api_key: Optional[str] = os.getenv("MISTRAL_API_KEY")
        self.ai_model: Optional[str] = os.getenv("MISTRAL_AI_MODEL")
        self.validate_config()
        self.client: Mistral = Mistral(api_key=self.api_key)

    def validate_config(self) -> None:
        """Validate required environment variables."""

        if not self.api_key:
            print(
                "Error: MISTRAL_API_KEY not found in environment variables.",
                file=sys.stderr
            )
            sys.exit(1)

        if not self.ai_model:
            print(
                "Error: MISTRAL_AI_MODEL not found in environment variables.",
                file=sys.stderr
            )
            sys.exit(1)
    async def ask_ai(self) -> None:
        print("=================================")
        print("      Mistral AI Assistant")
        print("=================================")
        print("Ask the AI anything!")
        print("Type 'exit' to quit.")
        print()

        while True:
            try:
                # Get user input
                prompt: str = input("Ask AI: ").strip()

                # Exit the application
                if prompt.lower() == "exit":
                    print("Goodbye!")
                    break

                # Ignore empty input
                if not prompt:
                    print("Please enter a question.")
                    continue

                # Add user prompt to conversations
                self.conversations.append({"role": "user", "content": prompt})

                # Send request to Mistral
                response = await self.client.chat.stream_async(
                    model=self.ai_model,
                    messages=[
                       {
                            "role": "system",
                            "content": "You are a helpful study buddy. You will be provided with class problems"
                       },
                       *self.conversations # Include previous conversations
                    ]
                )

                assert response
                ai_response_content = ""
                async for chunk in response:
                    if chunk.data.choices[0].delta.content is not None:
                        content_part = chunk.data.choices[0].delta.content
                        ai_response_content += content_part
                        print(content_part, end="")

                print("\n")
                # Add AI response to conversations
                self.conversations.append({"role": "assistant", "content": ai_response_content})

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break

            except Exception as e:
                print(f"\nAn error occurred: {e}\n")


def main() -> None:
    """Main entry point."""
    study_buddy = StudyBuddy()
    asyncio.run(study_buddy.ask_ai())


if __name__ == "__main__":
    main()
