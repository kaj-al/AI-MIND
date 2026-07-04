from config import llm

def calc_confidence(query,evidence):
    prompt = f"""
          Analyze the claim and supporting evidence
          claim:{query}
          evidence:{evidence}
          return only confidence score between 0 and 100
"""
    response = llm.invoke(prompt)
    return response.content

