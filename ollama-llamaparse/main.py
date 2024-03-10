import chromadb
import nest_asyncio
import os

from dotenv import load_dotenv
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

load_dotenv()
nest_asyncio.apply()


llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
parser = LlamaParse(
    api_key=llamaparse_api_key,
    result_type="markdown",
)
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(
    input_files=["data/claude.pdf"], file_extractor=file_extractor
).load_data()

print("===== Loaded Data =====")

embed_model = OllamaEmbedding(
    model_name="llama2",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)
llm = Ollama(model="mistral", request_timeout=30.0)
Settings.llm = llm
Settings.embed_model = embed_model

print("===== Loaded LLM =====")

db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, embed_model=embed_model
)

print("===== Loaded Vector Store =====")

db2 = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db2.get_or_create_collection("quickstart")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)

print("===== Loaded Index =====")

query_engine = index.as_query_engine()
query = "What are the 3 Claude models?"
response = query_engine.query(query)

print(response)
