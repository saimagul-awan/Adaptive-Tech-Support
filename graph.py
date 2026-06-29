from langgraph.graph import StateGraph, END

from state import GraphState

from agents import (
    rewrite_query,
    retrieve_documents,
    grade_documents,
    web_search,
    generate_answer,
    check_hallucination,
)


# -----------------------------
# Rewrite Query
# -----------------------------
def rewrite_node(state: GraphState):

    optimized = rewrite_query(state["original_query"])

    state["optimized_query"] = optimized

    return state


# -----------------------------
# Retrieve Documents
# -----------------------------
def retrieve_node(state: GraphState):

    docs = retrieve_documents(state["optimized_query"])

    state["documents"] = docs

    return state


# -----------------------------
# Grade Retrieved Documents
# -----------------------------
def grade_node(state: GraphState):

    score = grade_documents(
        state["original_query"],
        state["documents"]
    )

    state["relevance_score"] = score

    return state


# -----------------------------
# Web Search
# -----------------------------
def websearch_node(state: GraphState):

    docs = web_search(state["original_query"])

    state["documents"] = docs

    return state


# -----------------------------
# Generate Answer
# -----------------------------
def generate_node(state: GraphState):

    docs = state["documents"]

    # Convert LangChain Documents to text
    if len(docs) > 0 and hasattr(docs[0], "page_content"):
        docs = [doc.page_content for doc in docs]

    answer = generate_answer(
        state["original_query"],
        docs
    )

    state["generation"] = answer

    return state


# -----------------------------
# Hallucination Check
# -----------------------------
def hallucination_node(state: GraphState):

    docs = state["documents"]

    if len(docs) > 0 and hasattr(docs[0], "page_content"):
        docs = [doc.page_content for doc in docs]

    result = check_hallucination(
        docs,
        state["generation"]
    )

    state["hallucination_check"] = result

    return state


# -----------------------------
# Route after grading
# -----------------------------
def route_after_grade(state: GraphState):

    if state["relevance_score"].lower() == "yes":
        return "generate"

    return "websearch"


# -----------------------------
# Route after hallucination
# -----------------------------
def route_after_hallucination(state: GraphState):

    if state["hallucination_check"].lower() == "passed":
        return END

    if state.get("loop_count", 0) >= 2:
        return END

    state["loop_count"] = state.get("loop_count", 0) + 1

    return "generate"


# -----------------------------
# Build Graph
# -----------------------------
workflow = StateGraph(GraphState)

workflow.add_node("rewrite", rewrite_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_node)
workflow.add_node("websearch", websearch_node)
workflow.add_node("generate", generate_node)
workflow.add_node("hallucination", hallucination_node)

workflow.set_entry_point("rewrite")

workflow.add_edge("rewrite", "retrieve")
workflow.add_edge("retrieve", "grade")

workflow.add_conditional_edges(
    "grade",
    route_after_grade,
    {
        "generate": "generate",
        "websearch": "websearch",
    },
)

workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", "hallucination")

workflow.add_conditional_edges(
    "hallucination",
    route_after_hallucination,
    {
        "generate": "generate",
        END: END,
    },
)

graph = workflow.compile()
