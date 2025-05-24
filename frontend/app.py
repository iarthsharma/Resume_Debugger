### resume_debugger_tool/frontend/app.py

import streamlit as st
import requests

st.title("AI-Powered Resume Debugger")

resume_text = st.text_area("Paste your resume text here:")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        response = requests.post("http://backend:8000/analyze", json={"text": resume_text})
        result = response.json()
        st.subheader("Detected Anomalies")
        st.write(result["anomalies"])
        st.subheader("Suggested Improvements")
        st.write(result["suggestions"])
