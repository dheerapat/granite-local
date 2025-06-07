from openai import OpenAI


def make_request(instruction: str):
    client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

    response = client.chat.completions.create(
        model="granite-3.3-8b-instruct",
        messages=[{"role": "user", "content": instruction}],
    )

    return response.choices[0].message.content


print(make_request("step by step guide to cook a dish called shakshuka"))
