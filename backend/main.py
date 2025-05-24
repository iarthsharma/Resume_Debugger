### resume_debugger_tool/backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ResumeInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_resume(resume: ResumeInput):
    anomalies = detect_anomalies(resume.text)
    suggestions = get_chatgpt_suggestions(resume.text, anomalies)
    log_to_db(resume.text, anomalies, suggestions)
    return {"anomalies": anomalies, "suggestions": suggestions}

def detect_anomalies(text):
    issues = []
    if "team player" in text.lower():
        issues.append("Generic phrase: 'team player'")
    if len(text.split(".")) < 5:
        issues.append("Too few bullet points or accomplishments")
    if "%" not in text and "$" not in text and "increased" not in text.lower():
        issues.append("Missing quantifiable achievements")
    return issues

def get_chatgpt_suggestions(text, issues):
    prompt = f"Resume text:\n{text}\n\nIssues found: {issues}\n\nSuggest clear, quantifiable, and impactful edits:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message['content']

def log_to_db(text, issues, suggestions):
    conn = sqlite3.connect("backend/resume_logs.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resume_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume TEXT,
            anomalies TEXT,
            suggestions TEXT
        )
    """)
    cur.execute(
        "INSERT INTO resume_logs (resume, anomalies, suggestions) VALUES (?, ?, ?)",
        (text, str(issues), suggestions)
    )
    conn.commit()
    conn.close()