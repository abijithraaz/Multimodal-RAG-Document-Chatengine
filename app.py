import os
import openai
import streamlit as st
from llm_chat.openai_llm import OpenAiLLM
from input_preprocessor.preprocess_pdf2img import pdf_to_single_png
from llm_chat.azure_openai_llm import AzureOpenAiLLM
from llm_chat.aws_bedrock_llm import BedrockLLM
from prompt_augmentor import PromptAugmentor
from embedding.openai_embedd_generator import OpenaiEmbeddGenarator
from embedding.azure_openai_embedd_generator import AzureOpenaiEmbeddGenarator
from retriever.pinecone_data_retriever import PineconeDBRetriever
from retriever.mongo_data_retriever import MongoDBRetriever


# Env variables
os.environ['AZURE_OPENAI_API_KEY'] = ""
os.environ['AZURE_OPENAI_ENDPOINT'] = ""
os.environ['AZURE_OPENAI_EMBEDD_MODEL'] = ''
os.environ['OPENAI_API_VERSION'] = ''
os.environ['OPENAI_EMBEDD_DEPLOY'] = ''

os.environ['PINECONE_API_KEY'] = ''
os.environ['PINECONE_ENVIRONMENT'] = ''
os.environ['PINECONE_INDEX_NAME'] = ''

os.environ['MONGODB_URI'] = ""
os.environ['MONGODB_NAME'] = ''
os.environ['MONGODB_COLLECTION'] = ''
os.environ['MONGO_INDEX_NAME'] = ''

os.environ['LLAMA_CLOUD_API_KEY'] = ''


# calling prompt augmentor
rag_client = PromptAugmentor()

# embedd = OpenaiEmbeddGenarator()
embedd = AzureOpenaiEmbeddGenarator()

# retriever
retriever = MongoDBRetriever()

# UI section
st.header(body='Doc Chatengine 🤗💬', divider='rainbow')
st.markdown(body= 'Chatengine wil help you to communicate your documents.')
st.subheader(body='Model Provider Selection')

# Selection of services
option = st.selectbox(
            'Please select the model provider you want to try?',
            ('AzureOpenAIModel', 'AWSBedrockModel')
            )

if option == 'AWSBedrockModel':
    chatengine = BedrockLLM()
else:
    chatengine = AzureOpenAiLLM()

# file uploader
img_file_buffer = st.file_uploader('Upload a PNG image or pdf', type=['png','pdf'])
if img_file_buffer and img_file_buffer.name.endswith(('.pdf', '.PDF')):
    img_file = pdf_to_single_png(img_file_buffer.read())
    print(type(img_file_buffer))
elif img_file_buffer:
    img_file = img_file_buffer.read()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display history of app
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# Accept user input and process
if query := st.chat_input('Please write your query...'):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    retrieved_data = retriever.retrieve_data(embedd_client=embedd, query=query)
    if len(retrieved_data) !=0:
        with st.chat_message("retriever"):
            st.markdown(f"Source of Info:{retrieved_data}")
        st.session_state.messages.append({"role": "retriever", "content": f"Source of Info:{retrieved_data}"})

    # Chat response
    with st.chat_message('assistant'):
        # retrieved_data = retriever.retrieve_data(embedd_client=embedd, query=query)
        augmented_query = rag_client.augment_prompt(query, retrieved_data)
        if img_file_buffer:
            chat_response = chatengine.llmchat(augmented_query, encoded_image=img_file)
        else:
            # chat_response = chatengine.llmchat(query)
            chat_response = chatengine.llmchat(augmented_query)

        st.markdown(chat_response)
    # Adding response to history
    st.session_state.messages.append({"role":"assistant", "content":chat_response})

# Clear chat button
with st.sidebar:
    if button := st.button('CLEAR CHAT', type='primary',use_container_width=True):
        if "messages" in st.session_state:
            st.session_state.messages = []
        img_file_buffer = None

    
