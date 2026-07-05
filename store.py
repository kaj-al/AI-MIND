import os
import tempfile
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

PERSIST_DIRECTORY = "./vectorstore"
EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_db():
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=EMBEDDINGS,
    )


def store_documents(uploaded_files):
    files = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]
    files = [f for f in files if f is not None]

    if not files:
        return 0

    temp_paths = []
    all_docs = []

    try:
        for uploaded_file in files:
            if isinstance(uploaded_file, str):
                source_path = uploaded_file
            else:
                filename = getattr(uploaded_file, "name", "") or "document.pdf"
                suffix = Path(filename).suffix or ".pdf"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    if hasattr(uploaded_file, "getvalue"):
                        temp_file.write(uploaded_file.getvalue())
                    else:
                        temp_file.write(uploaded_file.read())
                    source_path = temp_file.name
                temp_paths.append(source_path)

            if os.path.exists(source_path):
                loader = PyPDFLoader(source_path)
                all_docs.extend(loader.load())

        if not all_docs:
            return 0

        db = get_db()
        db.add_documents(all_docs)
        db.persist()
        return len(all_docs)
    finally:
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                os.remove(temp_path)


upload = store_documents