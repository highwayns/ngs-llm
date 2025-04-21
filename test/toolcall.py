# Databricks notebook source
"""
函数调用支持
并行函数调用
gpt-35-turbo (1106)
gpt-35-turbo (0125)
gpt-4 (1106-Preview)
gpt-4 (0125-Preview)
gpt-4 (vision-preview)
gpt-4 (2024-04-09)
gpt-4o (2024-05-13)
gpt-4o (2024-08-06)
gpt-4o (2024-11-20)
gpt-4o-mini (2024-07-18)
gpt-4.5-preview (2025-02-27)
gpt-4.1 (2025-04-14)
gpt-4.1-nano (2025-04-14)
gpt-4.1-mini (2025-04-14)
o4-mini (2025-04-16)
o3 (2025-04-16)
API 版本 2023-12-01-preview 中首次添加了对并行函数的支持

使用工具进行基本函数调用
所有支持并行函数调用的模型
o3-mini (2025-01-31)
o1 (2024-12-17)
gpt-4 (0613)
gpt-4-32k (0613)
gpt-35-turbo-16k (0613)
gpt-35-turbo (0613)
"""
import os
import json
from openai import AzureOpenAI
from datetime import datetime
from zoneinfo import ZoneInfo

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2025-02-01-preview"
)

# Define the deployment you want to use for your chat completions API calls

deployment_name = "<YOUR_DEPLOYMENT_NAME_HERE>"

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}

def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    messages = [{"role": "user", "content": "What's the current time in San Francisco"}] # Single function call
    #messages = [{"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Paris?"}] # Parallel function call with a single tool/function defined

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "get_current_time":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")  
                time_response = get_current_time(
                    location=function_args.get("location")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_current_time",
                    "content": time_response,
                })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())

