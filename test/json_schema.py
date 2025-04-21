# Databricks notebook source
"""
JSON 模式支持
JSON 模式目前仅支持以下模型：

支持的型号
gpt-35-turbo(1106)
gpt-35-turbo(0125)
gpt-4（1106 预览版）
gpt-4（0125-预览）
gpt-4o
gpt-4o-mini
API 支持
对 JSON 模式的支持首次在 API 版本 2023-12-01-preview 中添加
"""
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2025-03-01-preview"
)

response = client.chat.completions.create(
  model="YOUR-MODEL_DEPLOYMENT_NAME", # Model = should match the deployment name you chose for your model deployment
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Who won the world series in 2020?"}
  ]
)
print(response.choices[0].message.content)
