from config import llm

def check_bias(perspective):
    prompt = f"""
        Analyze :{perspective}
    check:Psycophancy, unsupported assumptions, confirmation bias
"""
    return llm.invoke(prompt)