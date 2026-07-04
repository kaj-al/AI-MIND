from typing import TypedDict
from agents.claim_detector import detector
from agents.retriever import evidence 
from agents.perspective import gen_perspective
from agents.bias_checker import check_bias
from response import final
from agents.confidence import calc_confidence
from langgraph.graph import StateGraph, START,END

class Agent(TypedDict):
    query:str
    claim:str
    evidence:list
    sources:list
    perspective:str
    bias:str
    confidence:str
    ans:str

def claim_node(state): 
    claim_res = detector(state["query"])
    return{"claim":claim_res}

def retriever_node(state): 
    result = evidence(state["query"])
    return{"evidence":result["evidence"],"sources":result["sources"]}

def perspective_node(state):
    perspective_result = gen_perspective(
        state["query"],
        state["evidence"]
    )
    return {
        "perspective": perspective_result
    }

def bias_node(state):
    bias_result = check_bias(state["perspective"])
    return {
        "bias": bias_result
    }

def confidence_node(state):
    confidence = calc_confidence(state["query"],state["evidence"])
    return{"confidence":confidence}

def final_node(state):
    final_answer = final(
        state["query"],
        state["evidence"],
        state["sources"],      
        state["perspective"],
        state["bias"],
        state["confidence"]
    )
    return {
        "ans": final_answer
    }

graph = StateGraph(Agent)

graph.add_node("claim_detector",claim_node)
graph.add_node("retriever",retriever_node)
graph.add_node("perspective",perspective_node)
graph.add_node("bias_checker",bias_node)
graph.add_node("confidence",confidence_node)
graph.add_node("final_answer",final_node)

graph.add_edge(START,"claim_detector")
graph.add_edge("claim_detector","retriever")
graph.add_edge("retriever","perspective")
graph.add_edge("perspective","bias_checker")
graph.add_edge("bias_checker","confidence")
graph.add_edge("confidence","final_answer")
graph.add_edge("final_answer",END)

graph = graph.compile()