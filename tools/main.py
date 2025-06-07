from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam
from transformers.utils.chat_template_utils import get_json_schema

from get_stock_price import get_stock_price
from get_weather import get_weather

tools = [
    ChatCompletionToolParam(**tool)
    for tool in [get_json_schema(get_stock_price), get_json_schema(get_weather)]
]


def make_request(instruction: str):
    client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

    response = client.chat.completions.create(
        model="granite-3.3-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant with access to the following function calls. Your task is to produce a list of function calls necessary to generate response to the user utterance. Use the following function calls as required.",
            },
            {"role": "user", "content": instruction},
        ],
        tool_choice="auto",
        tools=tools,
    )
    if response.choices[0].message.tool_calls is not None:
        return response.choices[0].message.tool_calls[0].function
    else:
        return None


if __name__ == "__main__":
    query = "What were the IBM stock prices on October 7, 2024?"
    print(make_request(query))
