@echo off
REM ------------------------------
REM Quote Videos Phase-1 Runner
REM ------------------------------
REM 1) Create venv
REM 2) Install requirements
REM 3) Run generator
REM NOTE: FFmpeg must be installed and available in PATH.
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python make_videos.py
pause
