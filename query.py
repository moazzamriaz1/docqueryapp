import streamlit as st
import os
import openai
import PyPDF2
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain import VectorDBQA
from langchain.document_loaders import UnstructuredFileLoader, UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import nltk
from streamlit_chat import message


nltk.download("punkt")


def run_query_app(username):
    openai_api_key = st.sidebar.text_input("OpenAI API Key", key="openai_api_key_input", type="password")

    uploaded_file = st.file_uploader("Upload a file", type=['txt', 'pdf'], key="file_uploader")
    if uploaded_file:
        # Save the uploaded file
        file_path = os.path.join('./uploaded_files', uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Initialize OpenAIEmbeddings

        os.environ['OPENAI_API_KEY'] = openai_api_key

        # Initialize OpenAIEmbeddings
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

        # Load the file as document
        _, ext = os.path.splitext(file_path)
        if ext == '.txt':
            loader = UnstructuredFileLoader(file_path)
        elif ext == '.pdf':
            loader = UnstructuredPDFLoader(file_path)
        else:
            st.write("Unsupported file format.")
            return

        documents = loader.load()

        # Split the documents into texts
        text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # Create Chroma vectorstore from documents
        doc_search = Chroma.from_documents(texts, embeddings)

        # Initialize VectorDBQA
        chain = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=doc_search)

        if 'messages' not in st.session_state:
            st.session_state['messages'] = []

        if 'past' not in st.session_state:
            st.session_state['past'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = []

        def update_chat(messages, sender, text):
            message = {'sender': sender, 'text': text}
            messages.append(message)
            return messages

        def get_response(chain, messages):
            input_text = [m['text'] for m in messages if m['sender'] == 'user']
            result = chain.run(input_text[-1])
            return result

        def get_text():
            input_text = st.text_input("You: ", key="input")
            return input_text

        query = get_text()
        user_input = query

        if st.button("Run Query"):
            with st.spinner("Generating..."):
                messages = st.session_state.get('messages', [])
                messages = update_chat(messages, "user", query)
                response = get_response(chain, messages)
                messages = update_chat(messages, "assistant", response)
                st.session_state['messages'] = messages
                st.session_state['past'].append(query)
                st.session_state['generated'].append(response)
        if uploaded_file is not None:
            message(f"You are chatting with {uploaded_file.name}. Ask anything about it?")
        if st.session_state['generated']:

            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state['generated'][i], key=str(i))

            with st.expander("Show Messages"):
                for i, msg in enumerate(st.session_state['messages']):
                    if msg['sender'] == 'user':
                        message("User", msg['text'], key=f"user_{i}")
                    else:
                        message("Assistant", msg['text'], key=f"assistant_{i}")







    if __name__ == '__main__':
        run_query_app()
