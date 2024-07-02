from openai import OpenAI
import openai
import os

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

# def function_without_list_comp():
#     my_list = [1, 2, 3]
#     squared_list = []
#     for x in my_list:
#         squared_list.append(x**2)  # Regular loop
#     return squared_list

# def function_without_list_comp(): #     my_list = [1, 2, 3] #     squared_list = [] #     for x in my_list: #         squared_list.append(x**2)  # Regular loop #     return squared_list

messages = [
            {"role": "system", "content": "You are a helpful assistant that helps me breaks down the meaning of functions."},
            {"role": "user", "content": " # def function_without_list_comp(): #     my_list = [1, 2, 3] #     squared_list = [] #     for x in my_list: #         squared_list.append(x**2)  # Regular loop #     return squared_list "}, 
            {"role": "user", "content": "Break down line by line what this function does, and also evaluate the in line comments?"}
        ]


def get_response():  
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    # print(response.choices[0])
    return response.choices[0].message.content

print(get_response())