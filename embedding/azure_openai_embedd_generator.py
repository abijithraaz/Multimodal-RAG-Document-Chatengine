import os
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings

from embedding.base_embedd_generator import BaseEmbeddGenarator

class AzureOpenaiEmbeddGenarator(BaseEmbeddGenarator):
    def __init__(self) -> None:
        self.embed = AzureOpenAIEmbeddings(azure_deployment=os.getenv('OPENAI_EMBEDD_DEPLOY'), azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                                           api_key=os.getenv('AZURE_OPENAI_API_KEY'), api_version=os.getenv('OPENAI_API_VERSION'))

    def embedd_generator(self, data_frame):
        # openai ada embedding
        def get_embedding(text):
            return self.embed.embed_query(text) 
        
        for data in data_frame['text']:
            data_frame['embeddings'] = [get_embedding(data)]
        return data_frame
