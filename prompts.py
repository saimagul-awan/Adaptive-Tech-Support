rewrite_prompt = """
You are a technical support expert.

Rewrite the user's question into a keyword-rich search query.

Return ONLY the rewritten query.

Question:
{question}
"""

grading_prompt = """
You are a QA Engineer.

Determine whether the retrieved documents are relevant.

Return ONLY JSON.

{
    "relevance_score":"yes"
}

or

{
    "relevance_score":"no"
}

Question:
{question}

Documents:
{documents}
"""

generate_prompt = """
You are an expert technical support engineer.

Answer ONLY from the supplied context.

If the answer is not present in the context, say:

"I don't have enough information."

Context:

{context}

Question:

{question}
"""

hallucination_prompt = """
You are a QA Engineer.

Compare the answer against the documents.

Return ONLY JSON.

{
"hallucination_check":"passed"
}

or

{
"hallucination_check":"failed"
}

Documents:

{documents}

Answer:

{answer}
"""