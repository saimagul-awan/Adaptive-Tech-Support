from dotenv import load_dotenv
import os

load_dotenv()

import json
from duckduckgo_search import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import (
    rewrite_prompt,
    grading_prompt,
    generate_prompt,
    hallucination_prompt
)

from retriever import retriever

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# ---------------------------
# Rewrite Agent
# ---------------------------

def rewrite_query(question):

    prompt = rewrite_prompt.format(question=question)

    response = llm.invoke(prompt)

    return response.content


# ---------------------------
# Retrieve Agent
# ---------------------------

def retrieve_documents(query):

    return retriever.invoke(query)


# ---------------------------
# QA Agent
# ---------------------------

def grade_documents(question, documents):

    docs = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = grading_prompt.format(
        question=question,
        documents=docs
    )

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
        return result["relevance_score"]

    except:
        return "no"


# ---------------------------
# Web Search
# ---------------------------

def web_search(query):

    results = []

    with DDGS() as ddgs:

        search = ddgs.text(
            query,
            max_results=3
        )

        for item in search:
            results.append(item["body"])

    return results


# ---------------------------
# Generator
# ---------------------------

def generate_answer(question, docs):

    context = "\n\n".join(docs)

    prompt = generate_prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content


# ---------------------------
# Hallucination Checker
# ---------------------------

def check_hallucination(docs, answer):

    context = "\n\n".join(docs)

    prompt = hallucination_prompt.format(
        documents=context,
        answer=answer
    )

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
        return result["hallucination_check"]

    except:
        return "failed"