from config import llm

def gen_perspective(query,context):
    prompt = f"""
           User statement:{query}
           evidence:{context}
           generate:supporting perspective, opposing perspective, neutral_perspective
"""
    return llm.invoke(prompt)  
     
   
