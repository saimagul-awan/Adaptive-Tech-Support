from agents import *

question = "How do I reset the hub?"

optimized = rewrite_query(question)

print("Optimized Query:")
print(optimized)

docs = retrieve_documents(optimized)

print("\nRetrieved:", len(docs))

score = grade_documents(question, docs)

print("\nQA Score:", score)

pages = [doc.page_content for doc in docs]

answer = generate_answer(question, pages)

print("\nAnswer:\n")

print(answer)

check = check_hallucination(
    pages,
    answer
)

print("\nHallucination:", check)