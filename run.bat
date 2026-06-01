@echo off
echo ============================================
echo  AI-Powered Product Strategy Assistant
echo  Multi-Agent Analysis System
echo ============================================
echo.

REM Check if ANTHROPIC_API_KEY is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo WARNING: ANTHROPIC_API_KEY environment variable not set.
    echo You can also enter it in the app UI.
    echo.
)

echo Starting Streamlit application...
echo Open your browser at: http://localhost:8501
echo Press Ctrl+C to stop.
echo.

python -m streamlit run app.py --server.port 8501 --server.headless false
