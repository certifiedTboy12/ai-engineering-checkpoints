# Mistral AI Study Buddy

This project is a simple, command-line-based "Study Buddy" powered by the Mistral AI API. It allows you to interact with a Mistral model directly from your terminal, providing a helpful assistant for your study sessions or programming problems.

## Features

- **Interactive Chat**: Engage in a conversation with the Mistral AI from your terminal.
- **Streaming Responses**: Responses are streamed in real-time for a more dynamic experience.
- **Configurable**: Easily set your API key and desired model using an environment file.
- **Context-Aware**: Uses a system prompt to frame the AI as a helpful study assistant.
- **Robust Error Handling**: Gracefully handles configuration errors and interruptions.

## Requirements

- Python 3.7+
- An active Mistral AI API key.

## Setup and Installation

Follow these steps to get the Study Buddy running on your local machine.

### 1. Clone the Repository

If this were a git repository, you would clone it. For now, just ensure you have the `study_buddy.py` file.

### 2. Install Dependencies

The script relies on a few Python packages. You can install them using pip. It's recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required packages
pip install mistralai python-dotenv
```

### 3. Configure Environment Variables

The application requires you to set your Mistral API key and the model you wish to use.

1.  Create a file named `.env` in the same directory as `study_buddy.py`.
2.  Add the following lines to the `.env` file, replacing the placeholder values with your own:

    ```env
    MISTRAL_API_KEY="YOUR_API_KEY_HERE"
    MISTRAL_AI_MODEL="mistral-large-latest"
    ```

    > **Note:** You can use any other compatible model name for `MISTRAL_AI_MODEL`, such as `mistral-small-latest`.

## Usage

Once the setup is complete, run the script from your terminal:

```bash
python study_buddy.py
```

You will be greeted with a welcome message and a prompt to ask your question.

```
=================================
      Mistral AI Assistant
=================================
Ask the AI anything!
Type 'exit' to quit.

Ask AI:
```

To stop the application, simply type `exit` and press Enter, or use `Ctrl+C`.

## Code Implementation Overview

The application is encapsulated within the `StudyBuddy` class in `study_buddy.py`.

### `StudyBuddy` Class

- **`__init__(self)`**:
  - Loads environment variables (`MISTRAL_API_KEY`, `MISTRAL_AI_MODEL`) from the `.env` file using `python-dotenv`.
  - Calls `validate_config()` to ensure the necessary variables are set.
  - Initializes the `Mistral` client with the provided API key.

- **`validate_config(self) -> None`**:
  - This method checks if the `MISTRAL_API_KEY` and `MISTRAL_AI_MODEL` have been loaded successfully.
  - If either variable is missing, it prints an error message to `stderr` and exits the application to prevent runtime errors.

- **`async def ask_ai(self) -> None`**:
  - This is the core asynchronous method that runs the main application loop.
  - It prints a welcome banner and instructions.
  - It enters an infinite `while True` loop to continuously accept user input.
  - Inside the loop, it handles user input for exiting the app (`exit`) or empty prompts.
  - It calls the Mistral API using `self.client.chat.stream_async`, which returns an asynchronous generator.
  - A `system` message is included in the payload to instruct the AI to act as a "helpful study buddy."
  - It iterates through the response stream (`async for chunk in response`), printing each piece of the message content as it arrives.
  - It includes `try...except` blocks to gracefully handle `KeyboardInterrupt` (`Ctrl+C`) and other potential exceptions during the API call.

### Entry Point

- The `main()` function creates an instance of the `StudyBuddy` class and uses `asyncio.run()` to execute the `ask_ai` asynchronous method.
- The standard `if __name__ == "__main__":` block ensures that `main()` is called only when the script is executed directly.
