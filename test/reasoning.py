# Databricks notebook source
"""
区域可用性
型	地区	访问受限
o4-mini	美国东部 2 （全球标准）

瑞典中部 （全球标准）	无需访问请求即可使用此模型的核心功能。

请求访问：o4-mini 推理摘要功能
o3	美国东部 2 （全球标准）

瑞典中部 （全球标准）	请求访问：o3 受限访问模型应用程序
o3-mini	模型可用性。	此模型的访问不再受到限制。
o1	模型可用性。	此模型的访问不再受到限制。
o1-preview	模型可用性。	此模型仅适用于作为原始受限访问版本的一部分被授予访问权限的客户。我们目前不会扩展对 .o1-preview
o1-mini	模型可用性。	Global Standard 部署不需要访问请求。

标准（区域）部署目前仅适用于之前在发行版中被授予访问权限的选定客户。o1-preview
API & 功能支持
特征	O4-迷你， 2025-04-16	O3， 2025-04-16	O3-迷你， 2025-01-31	O1， 2024-12-17	O1-预览版， 2024-09-12	O1-迷你， 2024-09-12
API 版本	2025-04-01-preview	2025-04-01-preview	2024-12-01-preview或更高版本
（Recommended）2025-03-01-preview	2024-12-01-preview或更高版本
（Recommended）2025-03-01-preview	2024-09-01-preview或更高版本
（Recommended）2025-03-01-preview	2024-09-01-preview或更高版本
（Recommended）2025-03-01-preview
开发者消息	✅	✅	✅	✅	-	-
结构化输出	✅	✅	✅	✅	-	-
上下文窗口	输入： 200,000
输出： 100,000	输入： 200,000
输出： 100,000	输入： 200,000
输出： 100,000	输入： 200,000
输出： 100,000	输入： 128,000
输出： 32,768	输入： 128,000
输出： 65,536
推理努力	✅	✅	✅	✅	-	-
视力支持	✅	✅	-	✅	-	-
聊天完成 API	✅	✅	✅	✅	✅	✅
响应 API	✅	✅	-	-	-	-
功能/工具	✅	✅	✅	✅	-	-
并行工具调用	✅	✅	-	-	-	-
max_completion_tokens*	✅	✅	✅	✅	✅	✅
系统消息**	✅	✅	✅	✅	-	-
推理总结 ***	✅	✅	-	-	-	-
流	✅	✅	✅	-	-	-
*推理模型仅适用于 parameter 。max_completion_tokens


**最新的 o 系列型号支持系统消息，使迁移更容易。当您使用带有 、 、 的系统消息时，它将被视为开发者消息。您不应在同一个 API 请求中同时使用开发人员消息和系统消息。*o4-minio3o3-minio1

***对 chain-of-thought reasoning summary 的访问仅限于 。o4-mini

不支持
推理模型目前不支持以下各项：

temperature, , , , , , ,top_ppresence_penaltyfrequency_penaltylogprobstop_logprobslogit_biasmax_tokens
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

response = client.chat.completions.create(
    model="o1-new", # replace with the model deployment name of your o1-preview, or o1-mini model
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))