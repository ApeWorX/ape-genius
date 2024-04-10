import os
import anthropic

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my_api_key",
)
knowledge_base = ''
with open('knowledge-base.txt', 'r', encoding="utf-8") as file:
    knowledge_base = file.read()

response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens = 4000,
    temperature=0,
    messages=[
        {
            "role": "user",
            # example for ygenius
            "content": "Answer the question using the knowledge base"
        },
        {
            "role": "assistant",
            "content": ":"
        },
        {
            "role": "user",
            "content": knowledge_base
        },
        {
            "role": "assistant",
            "content": ":"
        },
        {
            "role": "user",
            # add your question here
            "content": "what is apeworx"
        }
    ],
)

bot_response = response.content[0].text

print(bot_response)
