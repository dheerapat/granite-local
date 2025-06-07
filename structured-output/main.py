from openai import OpenAI
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def make_request(instruction: str):
    client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

    response = client.beta.chat.completions.parse(
        model="granite-3.3-8b-instruct",
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": instruction},
        ],
        response_format=CalendarEvent,
    )

    return response.choices[0].message.parsed


print(make_request("Alice and Bob are going to a science fair on Friday."))
