import os

import streamlit as st
from preprocessor.langchain_processor import LangChainDataLoader, LangChainChunkCreator
from preprocessor.llama_parser_processor import LlamaParserDataLoader
from embedding.azure_openai_embedd_generator import AzureOpenaiEmbeddGenarator
from data_handling.pinecone_db_handler import PineconeDB
from data_handling.mongo_db_handler import MongoDB

embedd_creator = AzureOpenaiEmbeddGenarator()

# Using Mongodb to store the data
# db = PineconeDB()
db = MongoDB()

st.header('Chatbot Manager 💬👷',divider='rainbow')
st.markdown('We can customize the chatbot using this page')

st.subheader(body='Model Provider Selection')
# Selection of services
option = st.selectbox(
            'Please select the model provider you want to try?',
            ('AzureOpenAIModel', 'AWSBedrockModel')
            )

# dataloader = LangChainDataLoader()
# LlamaParser data loader
dataloader = LlamaParserDataLoader()

chunkscreator = LangChainChunkCreator()

# chcking service to save model embedding
if option == 'AWSBedrockModel':
    embedd_creator = AzureOpenaiEmbeddGenarator()
    # pass
else:
    embedd_creator = AzureOpenaiEmbeddGenarator()

st.markdown('Upload custom text file data to cutomize the chatbot')
input_file = st.file_uploader(label='inputs in txt', type=['pdf','ppt','xlsx','docx','.txt'])
button = st.button(label='Upload')

if input_file and button:
    loaded_data = dataloader.load_data(input_file)
    data_chunks = chunkscreator.create_chunks(loaded_data)
    vector_dataset = embedd_creator.embedd_generator(data_frame=data_chunks)
    print('VectorDataset:', vector_dataset.head(1))
    datawrite = db.vectordata_storing(vector_dataset, input_file.name)
    if datawrite:
        st.markdown('Chatbot customization and DB modifications are completed.')
