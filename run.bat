@echo off
echo Starting Artidicia - The Artificial Serendipity Engine...
call .venv\Scripts\activate
.venv\Scripts\python.exe -m streamlit run app.py
pause
