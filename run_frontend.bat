@echo off

:: activating env
echo using conda env: llm
conda activate llm

:: Printing Hello world
echo running the frontend code
streamlit run Frontend/App.py

:: Closing the program
echo Closing the program
pause