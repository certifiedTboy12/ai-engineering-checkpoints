# AI Learning Assistant

This is a command-line interface (CLI) application that acts as a helpful learning assistant, powered by an OpenAI model.

## Description

The script `main.py` allows you to ask questions from your terminal and receive answers from an AI assistant. The assistant is configured with a system prompt to provide clear, simple explanations suitable for beginners, use examples, and break down complex topics.

It displays the AI's response and the token usage for each query.

## Features

- Interactive chat loop in the terminal.
- Fetches API key from a secure `.env` file.
- Displays input, output, and total token usage for each interaction.
- Graceful error handling for common API issues like authentication failures and rate limits.

## Setup

### 1. Prerequisites

- Python 3

### 2. Installation

1.  Clone or download the repository.

2.  Install the required Python packages. It is recommended to use a virtual environment.

    ```sh
    pip install openai python-dotenv
    ```

### 3. Configure API Key

1.  Create a file named `.env` in the same directory as `main.py`.

2.  Add your OpenAI API key to the `.env` file:

    ```
    OPENAI_API_KEY="your_api_key_here"
    ```

## How to Run

Execute the main script from your terminal:

```sh
python main.py
```

## How to Use

1.  Once the program is running, you will see a `You:` prompt.
2.  Type your question and press Enter.
3.  The assistant's answer will be displayed, followed by token usage details.
4.  To exit the program, type `exit` or `quit` and press Enter.
