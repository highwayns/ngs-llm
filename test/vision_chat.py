# Databricks notebook source
"""
支持视觉的聊天模型是由 OpenAI 开发的大型多模态模型 （LMM），可以分析图像并为有关图像的问题提供文本回答。它们结合了自然语言处理和视觉理解。当前支持视觉的模型是 o1、GPT-4o、GPT-4o-mini 和 GPT-4 Turbo with Vision。
"""
import base64
from mimetypes import guess_type

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

# Example usage
image_path = '<path_to_image>'
data_url = local_image_to_data_url(image_path)
print("Data URL:", data_url)