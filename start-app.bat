@echo off
cd .env\Scripts
call activate.bat
cd ../..
IF EXIST params.txt (
    python.exe run-auto.py
) ELSE (
    python.exe main.py
)