from openai import OpenAI
import openai
import os

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

messages = [
            {"role": "system", "content": "You are a helpful assistant that helps me breaks down the meaning of functions."},
            {"role": "user", "content": "def example_function():\n return x*2"},
            {"role": "user", "content": "Break down line by line what this function does?"}
        ]


def get_response():  
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    # print(response.choices[0])
    return response.choices[0].message.content

print(get_response())