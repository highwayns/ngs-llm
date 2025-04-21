# Databricks notebook source
"""
使用本文了解如何在 Azure OpenAI 中使用计算机。Computer Use 是一种专门的 AI 工具，它使用专门的模型，该模型可以通过其 UI 与计算机系统和应用程序交互来执行任务。使用 Computer Use，您可以创建一个代理，该代理可以处理复杂的任务，并通过解释视觉元素并根据屏幕上的内容采取行动来做出决策。

Computer Use 提供：

自主导航：例如，打开应用程序、单击按钮、填写表单和导航多页工作流。
动态适应：解释 UI 更改并相应地调整作。
跨应用程序任务执行：跨基于 Web 的应用程序和桌面应用程序运行。
自然语言界面：用户可以用通俗易懂的语言描述任务，计算机使用模型确定要执行的正确 UI 交互。
请求访问权限
要访问该模型，需要注册，并且将根据 Microsoft 的资格标准授予访问权限。有权访问其他受限访问模型的客户仍需要请求此模型的访问权限。computer-use-preview

请求访问：computer-use-preview 受限访问模型应用程序

授予访问权限后，您需要为模型创建部署。

区域支持
“计算机使用”在以下区域提供：

eastus2
swedencentral
southindia
"""
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

#from openai import OpenAI
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2025-03-01-preview"
)

response = client.responses.create(
    model="computer-use-preview", # set this to your model deployment name
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
    }],
    input=[
        {
            "role": "user",
            "content": "Check the latest AI news on bing.com."
        }
    ],
    truncation="auto"
)

print(response.output)


## response.output is the previous response from the model
computer_calls = [item for item in response.output if item.type == "computer_call"]
if not computer_calls:
    print("No computer call found. Output from model:")
    for item in response.output:
        print(item)

computer_call = computer_calls[0]
last_call_id = computer_call.call_id
action = computer_call.action

# Your application would now perform the action suggested by the model
# And create a screenshot of the updated state of the environment before sending another response

response_2 = client.responses.create(
    model="computer-use-preview",
    previous_response_id=response.id,
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser" # other possible values: "mac", "windows", "ubuntu"
    }],
    input=[
        {
            "call_id": last_call_id,
            "type": "computer_call_output",
            "output": {
                "type": "input_image",
                # Image should be in base64
                "image_url": f"data:image/png;base64,{<base64_string>}"
            }
        }
    ],
    truncation="auto"
)
