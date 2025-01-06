import os
from retriever.pinecone_data_retriever import PineconeDBRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI

class PromptAugmentor:
    def __init__(self) -> None:
        pass

    def augment_prompt(self, query, retrived_info):

        mod_query = f"""You are an assistant for question-answering tasks. 
            Use the following pieces of retrieved data to answer the question. 
            Retrived data: {retrived_info} 

            If you don't know the answer, just say that you don't know.

            Use three sentences maximum and keep the answer concise.
            Question: {query}  
            Answer:
            """

        return mod_query
