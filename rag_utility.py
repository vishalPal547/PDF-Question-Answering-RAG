import os
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


# Load environment variables from .env file
load_dotenv()

working_dir = os.path.dirname(os.path.abspath((__file__)))

# Load the embedding model
# (model_name is set explicitly so behavior stays stable even if the
# library's internal default ever changes)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Load the GPT-OSS-120B model from Groq
# NOTE: llama-3.3-70b-versatile was decommissioned by Groq on Aug 16, 2026.
# openai/gpt-oss-120b is Groq's recommended replacement (see
# https://console.groq.com/docs/deprecations).
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Prompt used to answer questions from retrieved document chunks
qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Use the given context to answer the question. "
            "If you don't know the answer based on the context, say you don't know. "
            "Keep the answer concise.\n\nContext:\n{context}",
        ),
        ("human", "{input}"),
    ]
)


def process_document_to_chroma_db(file_name):
    # Load the PDF document using UnstructuredPDFLoader
    loader = UnstructuredPDFLoader(f"{working_dir}/{file_name}")
    documents = loader.load()
    # Split the text into chunks for embedding
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    # Store the document chunks in a Chroma vector database
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embedding,
        persist_directory=f"{working_dir}/doc_vectorstore"
    )
    return 0


def answer_question(user_question):
    # Load the persistent Chroma vector database
    vectordb = Chroma(
        persist_directory=f"{working_dir}/doc_vectorstore",
        embedding_function=embedding
    )
    # Create a retriever for document search
    retriever = vectordb.as_retriever()

    # Build a retrieval chain using the current (non-deprecated) LangChain API.
    # `RetrievalQA` (used previously) was deprecated in LangChain 0.1.17 in
    # favor of `create_retrieval_chain` + `create_stuff_documents_chain`.
    combine_docs_chain = create_stuff_documents_chain(llm, qa_prompt)
    qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

    response = qa_chain.invoke({"input": user_question})
    answer = response["answer"]

    return answer
