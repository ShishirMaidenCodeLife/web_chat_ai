@REM @echo off
@REM set USERNAME=shishirmaidenrocklife@gmail.com
@REM set PASSWORD=nrbshk666
@REM set VRCHAT_PATH="C:\Program Files (x86)\Steam\steamapps\common\VRChat\VRChat.exe"

@REM %VRCHAT_PATH% --username %USERNAME% --password %PASSWORD%

@echo off
set USERNAME=shishirmaidenrocklife@gmail.com
set PASSWORD=xyzabc
set VRCHAT_PATH="C:\Program Files (x86)\Steam\steamapps\common\VRChat\VRChat.exe"

REM Launch VRChat with specified parameters
start "" %VRCHAT_PATH% 

REM Wait for VRChat to open (adjust the time as needed)
timeout /t 10 /nobreak

REM Run the Python script to automate the login process
python vrchat_login.py

REM Close the command prompt window when done (optional)
exit
