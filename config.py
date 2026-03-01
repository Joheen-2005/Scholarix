import streamlit as st
if "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY not configured in Streamlit secrets.")
    st.stop()
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
