from openai import OpenAI

client = OpenAI(base_url="http://192.168.110.142:1234/v1", api_key="local")

response = client.embeddings.create(
    input="Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world.",
    model="text-embedding-granite-embedding-278m-multilingual",
)

print(response.data[0].embedding)
