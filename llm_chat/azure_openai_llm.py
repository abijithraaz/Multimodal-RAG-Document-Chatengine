import os
import base64
from openai import  AzureOpenAI
from llm_chat.base_llm import BaseLLM

class AzureOpenAiLLM(BaseLLM):
    def __init__(self) -> None:
        self.client = AzureOpenAI(# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
                                    api_version=os.getenv('OPENAI_API_VERSION'),
                                    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
                                    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                                    api_key=os.getenv('AZURE_OPENAI_API_KEY'),)

    def llmchat(self, prompt: str, encoded_image=None) -> str:
        model ="" # replace your model deployment name

        def encode_image(image_path):
            encoded_image = base64.b64encode(image_path).decode('ascii')
            return encoded_image
        
        if encoded_image:
            messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that extracts information from the document."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(encoded_image)}"
                        }
                    },
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
            ]
        else:
            messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that extracts information from the document."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
            ]
        try: 
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.25,
            )
            resp_json =  response.choices[0].message.content
            return resp_json
        except Exception as e:
            print('Azureopenai exception:',e)
        
