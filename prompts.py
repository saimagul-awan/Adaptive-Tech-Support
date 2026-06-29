rewrite_prompt = """
You are a technical support expert.

Rewrite the user's question into a keyword-rich search query.

Return ONLY the rewritten query.

Question:
{question}
"""

grading_prompt = """
You are a relevance grader.

Question:
{question}

Documents:
{documents}

Respond ONLY with valid JSON.

{{
  "relevance_score": "yes"
}}

Return "yes" if the documents are relevant.
Return "no" otherwise.
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
