from typing import TypedDict, List

class GraphState(TypedDict):
    original_query: str
    optimized_query: str
    documents: List[str]
    generation: str
    relevance_score: str
    hallucination_check: str
    loop_count: int