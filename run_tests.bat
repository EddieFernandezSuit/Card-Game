@echo off
python -m py_compile network.py
if errorlevel 1 exit /b 1
python test_network_framing.py
if errorlevel 1 exit /b 1
echo All tests passed.

