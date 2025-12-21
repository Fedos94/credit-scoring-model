@echo off
echo Starting Docker Desktop...

:: Try different possible installation paths
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    echo Found Docker in Program Files
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    goto wait
)

if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
    echo Found Docker in Program Files
    start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    goto wait
)

if exist "%LocalAppData%\Docker\Docker Desktop.exe" (
    echo Found Docker in Local AppData
    start "" "%LocalAppData%\Docker\Docker Desktop.exe"
    goto wait
)

echo ❌ Docker Desktop not found!
echo Please install Docker Desktop from:
echo https://www.docker.com/products/docker-desktop/
goto end

:wait
echo.
echo Docker Desktop is starting...
echo Please wait 30-60 seconds for it to fully start...
echo Then run: scripts\check_docker.bat

:end
pause