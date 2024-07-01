from openai import OpenAI
import openai
import os

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions about programming."},
            {"role": "user", "content": "Can you explain what a Python dictionary is?"},
            {"role": "assistant", "content": "Sure! A Python dictionary is a collection of key-value pairs. It is used to store data values like a map, unlike other data types that hold only a single value as an element. A dictionary is defined using curly braces {}."},
            {"role": "user", "content": "How do you add a new key-value pair to a dictionary?"}
        ]


def get_response():  
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    return response.choices[0].message.content

print(get_response())