# Databricks notebook source
"""
模型支持
gpt-4o-mini版本：2024-07-18
gpt-4o版本：2024-08-06
gpt-4o版本：2024-11-20
gpt-4.1版本：2025-04-14
API 支持
2025-01-01-preview
不支持的功能
Predicted outputs 当前为纯文本。这些特征不能与参数和预测输出结合使用。prediction

工具/函数调用
音频模型/输入和输出
n值高于1
logprobs
presence_penalty大于0
frequency_penalty大于0
max_completion_tokens
"""
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-01-01-preview"
)

code = """
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
"""

instructions = """
Replace string `FizzBuzz` with `MSFTBuzz`. Respond only 
with code, and with no markdown formatting.
"""


completion = client.chat.completions.create(
    model="gpt-4o-mini", # replace with your unique model deployment name
    messages=[
        {
            "role": "user",
            "content": instructions
        },
        {
            "role": "user",
            "content": code
        }
    ],
    prediction={
        "type": "content",
        "content": code
    }
)

print(completion.model_dump_json(indent=2))
