from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

loader = PyPDFLoader("NexoraMinor.pdf")
docs = loader.load()
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./vectorstore"
)
db.persist()