from langgraph.graph import StateGraph, END

from state import GraphState

from agents import (
    rewrite_query,
    retrieve_documents,
    grade_documents,
    web_search,
    generate_answer,
    check_hallucination
)

def rewrite_node(state):
    print(">>> rewrite_node")
    optimized = rewrite_query(state["original_query"])
    state["optimized_query"] = optimized
    return state


def retrieve_node(state):
    print(">>> retrieve_node")
    docs = retrieve_documents(
        state["optimized_query"]
    )

    state["documents"] = docs

    return state

def grade_node(state):
print(">>> grade_node")
    score = grade_documents(
        state["original_query"],
        state["documents"]
    )

    state["relevance_score"] = score

    return state

def websearch_node(state):
print(">>> websearch_node")
    results = web_search(
        state["original_query"]
    )

    state["documents"] = results

    return state

def generate_node(state):
print(">>> generate_node")
    docs = state["documents"]

    if len(docs) > 0 and hasattr(docs[0], "page_content"):
        docs = [d.page_content for d in docs]

    answer = generate_answer(
        state["original_query"],
        docs
    )

    state["generation"] = answer

    return state
    
def hallucination_node(state):
print(">>> hallucination_node")
    docs = state["documents"]

    if len(docs) > 0 and hasattr(docs[0], "page_content"):
        docs = [d.page_content for d in docs]

    result = check_hallucination(
        docs,
        state["generation"]
    )

    state["hallucination_check"] = result

    return state

def route_after_grade(state):

    if state["relevance_score"] == "yes":
        return "generate"

    return "websearch"

def route_after_hallucination(state):

    if state["hallucination_check"] == "passed":
        return END

    if state["loop_count"] >= 2:
        return END

    state["loop_count"] += 1

    return "rewrite"

workflow = StateGraph(GraphState)

workflow.add_node("rewrite", rewrite_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_node)
workflow.add_node("websearch", websearch_node)
workflow.add_node("generate", generate_node)
workflow.add_node("hallucination", hallucination_node)

workflow.set_entry_point("rewrite")

workflow.add_edge(
    "rewrite",
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "grade"
)

workflow.add_edge(
    "websearch",
    "generate"
)

workflow.add_edge(
    "generate",
    "hallucination"
)

workflow.add_conditional_edges(
    "grade",
    route_after_grade,
    {
        "generate": "generate",
        "websearch": "websearch"
    }
)

workflow.add_conditional_edges(
    "hallucination",
    route_after_hallucination,
    {
        "rewrite": "rewrite",
        END: END
    }
)

graph = workflow.compile()

