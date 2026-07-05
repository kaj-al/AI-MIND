from store import get_db


def _get_retriever():
    db = get_db()
    return db.as_retriever()


def retrieve(query):
    retriever = _get_retriever()
    docs = retriever._get_relevant_documents(query)
    return docs


def evidence(query):
    retriever = _get_retriever()
    docs = retriever.invoke(query)
    evidence = []
    sources = []
    for doc in docs:
        evidence.append(doc.page_content)
        sources.append(doc.metadata.get("source", "Unknown"))
    return {"evidence": evidence, "sources": sources}