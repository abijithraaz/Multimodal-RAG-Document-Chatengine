import os
from typing import Dict
from llama_parse import LlamaParse
from langchain.document_loaders import TextLoader
from preprocessor.base_processor import DataLoader

class LlamaParserDataLoader(DataLoader):
    def __init__(self) -> None:
        pass

    def load_data(self, document_path) -> Dict:
        # To convert to a string based IO:
        doc_parsed = LlamaParse(result_type="markdown").load_data(document_path, extra_info={"file_name": "_"})
        
        # To read file as string:
        if len(doc_parsed) !=0:
            with open("./tmp/tmp_input.txt", "w") as f:
                f.write(doc_parsed[0].text)

        loader = TextLoader(r"./tmp/tmp_input.txt")
        documents = loader.load()
        return documents

'''
# Integration of azure model with llamaparse
parser = LlamaParse(
    result_type="markdown",
    use_vendor_multimodal_model=True,
    azure_openai_endpoint=f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME}/chat/completions?api-version=2024-10-01-preview",
    azure_openai_api_version="2024-10-01-preview",
    azure_openai_key=AZURE_OPENAI_API_KEY,
)
'''
