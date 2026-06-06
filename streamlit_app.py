import streamlit as st
from app import answer_question

st.set_page_config(page_title="Enterprise Policy Q&A Agent")
st.title("📄 Enterprise Policy Q&A Agent")

question = st.text_area("Enter your policy question")
country = st.text_input("Country (optional)")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching policies..."):
            result = answer_question(question, country or None)

        st.subheader("Answer")
        st.write(result["answer"])

        if result["citations"]:
            st.subheader("Sources")
            for c in result["citations"]:
                st.markdown(f"- `{c}`")

        st.metric("Confidence", f"{int(result['confidence'] * 100)}%")
