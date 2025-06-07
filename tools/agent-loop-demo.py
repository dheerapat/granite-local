"""
This file is AI generated. Reviewed by human
"""

import json
from typing import List, Optional
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionToolParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionMessageToolCallParam,
)
from openai.types.chat.chat_completion_message_tool_call_param import Function
from transformers.utils.chat_template_utils import get_json_schema

from get_stock_price import get_stock_price
from get_weather import get_weather

# Tool registry - maps function names to actual functions
TOOL_REGISTRY = {
    "get_stock_price": get_stock_price,
    "get_weather": get_weather,
}

tools = [
    ChatCompletionToolParam(**tool)
    for tool in [get_json_schema(get_stock_price), get_json_schema(get_weather)]
]


def execute_tool_call(tool_call):
    """Execute a tool call and return the result"""
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    if function_name in TOOL_REGISTRY:
        try:
            result = TOOL_REGISTRY[function_name](**function_args)
            return str(result)
        except Exception as e:
            return f"Error executing {function_name}: {str(e)}"
    else:
        return f"Unknown function: {function_name}"


def convert_tool_calls(
    tool_calls: Optional[List] = None,
) -> List[ChatCompletionMessageToolCallParam]:
    """Convert tool calls from the response to the correct type"""
    if not tool_calls:
        return []

    return [
        ChatCompletionMessageToolCallParam(
            id=tc.id,
            function=Function(name=tc.function.name, arguments=tc.function.arguments),
            type="function",
        )
        for tc in tool_calls
    ]


def make_agent_request(instruction: str, max_iterations: int = 5):
    """
    Tool calling loop agent that can make multiple tool calls and respond to user
    """
    client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

    # Initialize conversation with system message and user query
    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="You are a helpful assistant with access to function calls. Use the available tools to gather information and provide comprehensive answers to user queries.",
        ),
        ChatCompletionUserMessageParam(role="user", content=instruction),
    ]

    iteration = 0

    while iteration < max_iterations:
        print(f"\n--- Iteration {iteration + 1} ---")

        # Make request to the model
        response = client.chat.completions.create(
            model="granite-3.3-8b-instruct",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # Add assistant's response to conversation
        messages.append(
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content=assistant_message.content,
                tool_calls=convert_tool_calls(assistant_message.tool_calls),
            )
        )

        # Check if model wants to make tool calls
        if assistant_message.tool_calls:
            print(
                f"Model wants to make {len(assistant_message.tool_calls)} tool call(s)"
            )

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                print(
                    f"Executing: {tool_call.function.name}({tool_call.function.arguments})"
                )

                # Execute the tool
                result = execute_tool_call(tool_call)
                print(f"Result: {result}")

                # Add tool result to conversation
                messages.append(
                    ChatCompletionToolMessageParam(
                        role="tool", content=result, tool_call_id=tool_call.id
                    )
                )

            iteration += 1
        else:
            # No more tool calls, model has final answer
            print("Model provided final response")
            return assistant_message.content

    # If we hit max iterations
    return "Maximum iterations reached. The assistant may not have completed the task."


def simple_tool_call_example(instruction: str):
    """
    Simplified version that handles a single tool call
    """
    client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

    # Initial request
    response = client.chat.completions.create(
        model="granite-3.3-8b-instruct",
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="You are a helpful assistant with access to function calls. Use them to answer user queries.",
            ),
            ChatCompletionUserMessageParam(role="user", content=instruction),
        ],
        tools=tools,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        # Execute the first tool call
        tool_call = assistant_message.tool_calls[0]
        result = execute_tool_call(tool_call)

        # Make second request with tool result
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content="You are a helpful assistant. Provide a comprehensive answer based on the tool results.",
            ),
            ChatCompletionUserMessageParam(role="user", content=instruction),
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content=assistant_message.content,
                tool_calls=convert_tool_calls(assistant_message.tool_calls),
            ),
            ChatCompletionToolMessageParam(
                role="tool", content=result, tool_call_id=tool_call.id
            ),
        ]

        final_response = client.chat.completions.create(
            model="granite-3.3-8b-instruct", messages=messages
        )

        return final_response.choices[0].message.content
    else:
        return assistant_message.content


# Example usage
if __name__ == "__main__":
    query = "What is the weather in Bangkok right now?"

    print("=== Full Agent Loop ===")
    result = make_agent_request(query)
    print(f"\nFinal Answer: {result}")

    print("\n" + ("=" * 50) + "\n")
    print("=== Simple Tool Call ===")
    simple_result = simple_tool_call_example(query)
    print(f"\nSimple Result: {simple_result}")
