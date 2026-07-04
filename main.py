from fastapi import FastAPI
from graph import graph

app = FastAPI()


def serialize_response(value):
    if isinstance(value, dict):
        return {k: serialize_response(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialize_response(v) for v in value]
    if hasattr(value, "content"):
        return value.content
    return value


@app.post("/chat")
def chat(query: str):
    result = graph.invoke({"query": query})
    return serialize_response(result)