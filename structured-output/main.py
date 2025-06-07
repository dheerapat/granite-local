from openai import OpenAI
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


class SearchEngineKeywords(BaseModel):
    keywords: list[str]


def make_request(instruction: str):
    client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

    response = client.beta.chat.completions.parse(
        model="granite-3.3-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are search engine export, you have unmatched skill in searching with the right keyword. From user question, extract a keyword suitable to use for query in search engine.",
            },
            {"role": "user", "content": instruction},
        ],
        response_format=SearchEngineKeywords,
    )

    return response.choices[0].message.parsed


if __name__ == "__main__":
    print(make_request("what is the target blood pressure for healthy population"))
