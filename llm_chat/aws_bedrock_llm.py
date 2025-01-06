import os
import boto3
import json
import base64
import requests
# from PIL import Image
import io
from llm_chat.base_llm import BaseLLM

class BedrockLLM(BaseLLM):
    def __init__(self):
        self.client = boto3.client(
                                    service_name='bedrock-runtime',
                                    region_name='eu-central-1',  # Replace with your preferred region
                                )

    def llmchat(self, prompt, encoded_image=None):
        model_name ="anthropic.claude-3-haiku" # replace your model preference
        if encoded_image:
            byte_image = encoded_image
            conversation = [
            {
                "role": "user",
                "content": [{"text": prompt}, {'image':{'format': 'png','source':{'bytes': byte_image}}}],
            }
            ]
        else:
            conversation = [
            {
                "role": "user",
                "content": [{"text": prompt},],
            }
            ]
        try:
            # Send the message to the model, using a basic inference configuration.
            response = self.client.converse(
                modelId=model_name,
                messages=conversation,
                inferenceConfig={"maxTokens":512,"temperature":0.25},
                additionalModelRequestFields={"top_k":100}
            )
        
            # Extract and print the response text.
            response_text = response["output"]["message"]["content"][0]["text"]
            return response_text
    
        except (Exception) as e:
            print(f"ERROR: Can't invoke '{model_name}'.")