from graph import graph

inputs = {

    "original_query":"How do I reset the hub?",

    "optimized_query":"",

    "documents":[],

    "generation":"",

    "relevance_score":"",

    "hallucination_check":"",

    "loop_count":0
}

result = graph.invoke(inputs)

print(result["generation"])