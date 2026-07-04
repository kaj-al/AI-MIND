from config import llm

def detector(claim):
    prompt = f"""
            Classify:{input}
            categories:fact,opinion,emotional
"""
    return llm.invoke(prompt)