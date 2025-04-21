# Databricks notebook source
"""
响应 API
API 支持
2025-03-01-preview或更高版本

区域可用性
响应 API 目前在以下区域提供：

澳大利亚东部
东都
东都2
法国中央
日本东方
挪威东部
南印度
瑞典中心
阿联酋北部
英国南方
西都
西都3
模型支持
gpt-4o（版本： ， ，2024-11-202024-08-062024-05-13)
gpt-4o-mini（版本：2024-07-18)
computer-use-preview
gpt-4.1（版本：2025-04-14)
gpt-4.1-nano（版本：2025-04-14)
gpt-4.1-mini（版本：2025-04-14)
o3（版本：2025-04-16)
o4-mini（版本：2025-04-16)
并非每个模型都在响应 API 支持的区域可用。查看模型页面了解模型区域的可用性。

 注意

当前不支持：

结构化输出
tool_choice
image_url指向 Internet 地址
Web 搜索工具也不受支持，并且不是 API 的一部分。2025-03-01-preview
使用 Responses API 时，还存在一个已知的视觉性能问题，尤其是在 OCR 任务中。作为临时解决方法，请将 image detail 设置为 。此问题解决后，本文将更新，并添加任何其他功能支持。high
"""
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.responses.input_items.list("resp_67d856fcfba0819081fd3cffee2aa1c0")

print(response.model_dump_json(indent=2))
