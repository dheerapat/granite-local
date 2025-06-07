# Granite 3.3 8B Local Development: OpenAI API Compatible Test

This repo is a template for building application using IBM opensource model, Granite by running it locally using LMStudio and programatically used it via OpenAI SDK.

So far, Granite is capable of structured output, function calling and normal conversation.

After clone this project into your machine, run the following command

```bash
uv sync

# normal chat completion call
uv run main.py

# structure output into pydantic type
uv run structured-output/main.py

# function calling
uv run tools/main.py
```

Make sure you are running LMStudio server mode and the server is reachable from your machine.