import streamlit as st
import traceback

from graph import graph

st.title("Adaptive Technical Support Assistant")

question = st.text_input("Enter your technical question:")

if st.button("Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Processing..."):

            inputs = {
                "original_query": question,
                "optimized_query": "",
                "documents": [],
                "generation": "",
                "relevance_score": "",
                "hallucination_check": "",
                "loop_count": 0
            }

            try:
                result = graph.invoke(inputs)

                st.success("Answer Generated")
                st.write(result["generation"])

            except Exception as e:
                st.error("An error occurred.")
                st.code(traceback.format_exc())
