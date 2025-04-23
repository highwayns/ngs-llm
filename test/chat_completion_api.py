# Databricks notebook source
"""
GPT-3.5-Turbo、GPT-4 和 GPT-4o 系列模型是针对对话界面进行优化的语言模型。
这些模型的行为与旧的 GPT-3 模型不同。以前的模型是文本输入和文本输出，这意味着它们接受提示字符串并返回完成以附加到提示。
但是，最新的模型是对话输入和消息输出。模型需要以特定聊天类脚本格式格式化的输入。它们返回一个 completion，该 completion 表示聊天中模型编写的消息。
此格式专为多轮次对话而设计，但也适用于非聊天场景。
"""
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-10-21",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)