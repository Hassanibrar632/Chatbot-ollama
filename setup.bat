@echo off

:: Printing Hello world
echo create conda env: llm
conda create -n llm python=3.10 pip -y

:: activating conda env
echo Activate env: llm
conda activate llm

:: Installing libraries in the env
echo Installing libraries in the env
pip install -r requirements.txt

:: Installing llama3.2 using ollama
echo Installing llama3.2 using ollama
ollama pull llama3.2:latest

:: Stop the system
echo Exiting the env and closing the setup
pause