### resume_debugger_tool/README.md

# AI-Powered Resume Debugger

## Description
Analyze resumes using AI and anomaly detection to suggest impactful, quantifiable edits.

## How to Run
1. Set your OpenAI API key in `.env` or via environment variable.
2. Paste your resume text and press Analyze.

## Tech Stack
- Streamlit (UI)
- FastAPI (backend)
- OpenAI ChatGPT API
- SQLite (logging)
- Docker (local deployment)

## API
- `POST /analyze` — Accepts resume text, returns anomalies and GPT-based suggestions.
