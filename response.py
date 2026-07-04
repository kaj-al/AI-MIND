from config import llm

def final(query,evidence,sources,perspective,bias,confidence):
    prompt = f"""
        Query:{query}
        Evidence:{evidence}
        Sources:{sources}
        Perspective:{perspective}
        bias:{bias}
        confidence:{confidence}
        generate balanced answer, do not blindly agree, ask for evidence when needed.

"""
    response = llm.invoke(prompt)
    return response.content


