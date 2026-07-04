from store import db

retriever = db.as_retriever()

def retrieve(query):
    docs = retriever._get_relevant_documents(query)
    return docs

def evidence(query):
    docs = retriever.invoke(query)
    evidence = []
    sources = []
    for doc in docs:
        evidence.append(doc.page_content)
        sources.append(doc.metadata.get("source","Unknown"))
    return{"evidence":evidence,
               "sources":sources}