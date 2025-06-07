# Granite 3.3 8B Local Development: OpenAI API Compatible Test

This repository provides a template for building applications using IBM's open-source Granite model, running it locally with LMStudio, and programmatically accessing it via the OpenAI SDK.

## Features

Granite is capable of:
- Structured output using Pydantic types
- Function calling for tool integration
- Normal conversational interactions

## Getting Started

### Prerequisites

1. Ensure you have `uv` installed
2. Install LMStudio and run it in server mode
3. Clone this repository to your local machine

### Installation

1. Navigate to the project directory:
   ```bash
   cd granite-local
   ```

2. Synchronize dependencies:
   ```bash
   uv sync
   ```

### Usage

#### Normal Chat Completion
To run a basic chat completion:
```bash
uv run main.py
```

#### Structured Output
To get structured output in Pydantic format:
```bash
uv run structured-output/main.py
```

#### Function Calling
To use function calling capabilities:
```bash
uv run tools/main.py
```

## Project Structure

- `main.py`: Entry point for normal chat completion
- `structured-output/`: Contains code for structured output using Pydantic
- `tools/`: Contains function calling examples
- `embedding/`: (Optional) For embedding-related functionality

## Configuration

Make sure LMStudio is running in server mode and is reachable from your machine. You may need to configure the server URL in the respective Python files.