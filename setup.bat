@echo off

:: Printing Hello world
echo create conda env: llm
conda create -n llm python=3.10 pip -y

:: activating conda env
echo Activate env: llm
conda activate llm

:: Stop the system
echo Exiting the env and closing the setup
pause