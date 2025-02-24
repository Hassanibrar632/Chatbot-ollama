@echo off

:: activating env
echo using conda env: llm
conda activate llm

:: Printing Hello world
echo running the backend_code
python Backend/api.py

:: Closing the program
echo Closing the program
pause