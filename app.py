import streamlit as st
import traceback
from graph import graph

st.set_page_config(
    page_title="Adaptive Technical Support",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Adaptive Technical Support Assistant")

st.markdown("""
This assistant answers questions using:

- 📘 Orion SmartHub Manual (RAG)
- 🌐 Web Search (if documentation is insufficient)
- ✅ QA Relevance Checking
- 🧠 Hallucination Detection
- 🔄 LangGraph Workflow
""")

question = st.text_input(
    "Enter your technical question:"
)

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

                st.subheader("Answer")
                st.write(result["generation"])

                st.subheader("Workflow Details")

                st.write("**Optimized Query:**")
                st.code(result["optimized_query"])

                st.write("**Relevance Score:**")
                st.code(result["relevance_score"])

                st.write("**Hallucination Check:**")
                st.code(result["hallucination_check"])



except Exception as e:
    st.error("An error occurred while processing your request.")
    st.code(traceback.format_exc())
