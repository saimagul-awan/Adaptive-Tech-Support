from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Change this path if your file is in a different location
file_path = "orion_hub_manual .txt"

print("File exists:", os.path.exists(file_path))

# Load the document
loader = TextLoader(file_path)
docs = loader.load()

print("Documents loaded:", len(docs))

# Split the document
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100
)

splits = splitter.split_documents(docs)

print("Number of chunks:", len(splits))

# Create embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create ChromaDB
db = Chroma.from_documents(
    splits,
    embedding,
    persist_directory="chroma_db"
)

retriever = db.as_retriever(search_kwargs={"k": 3})

print("Retriever created successfully!")