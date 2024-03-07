import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA

# from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader

# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Load environment variables from .env file (Optional)
load_dotenv()

# Optional
# OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")


def main():
    st.title("Chat with Website")
    st.subheader(
        "Input your website URL, ask questions, and receive answers from the website. No nested URLs supported."
    )
    url = st.text_input("Insert The website URL")
    prompt = st.text_input("Ask a question (query/prompt)")
    if st.button("Submit Query", type="primary"):
        # Step 1: Load data from URL into vector DB
        loader = WebBaseLoader(url)
        data = loader.load()
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=40
        )
        docs = text_splitter.split_documents(data)
        ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=ollama_embeddings,
            collection_name="ollama_embeds",
        )
        vectordb.persist()

        # Step 2: Read data from vector DB
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        llm = Ollama(model="mistral")
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        response = qa(prompt)
        st.write(response)


if __name__ == "__main__":
    main()
