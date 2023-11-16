import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

knowledge_base = ''
with open('knowledge-base.txt', 'r', encoding="utf-8") as file:
    knowledge_base = file.read()

response = openai.chat.completions.create(
    model="gpt-4-1106-preview",
    temperature=0,
    messages=[
        {
            "role": "system",
            # example for ygenius
            "content": "You are a bot helping people understand Yearn Finance (aka Yearn). I have prefixed documents that help you understand what is Yearn, answer the user question using the source files and tell the source of your answer. The answer must exist within the source files, otherwise don't answer. You can use ```language to write code that shows in a pretty way. If the task is of creative nature it's ok to go wild and beyons just the sources, but MUST state that the answer is creative if this happens. Do not invent anything about ape that is not in source files unless you said you were going creative. False certanty about what ape can do is the worse thing you can do, avoid it at all costs."
        },
        {
            "role": "user",
            "content": knowledge_base
        },
        {
            "role": "user",
            # add your question here
            "content": "What can you do to help me explore Yearn?"
        }
    ],
)

bot_response = response.choices[0].message.content

print(bot_response)