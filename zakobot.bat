@echo off
:start
"C:\Users\Jaxom\AppData\Local\Programs\Python\Python38\python.exe" "B:\branchDev\zakobot.py"
timeout 10
echo Zako is detected to be offline. Restarting...
goto start
