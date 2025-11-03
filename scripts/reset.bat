@echo off
echo ========================================
echo Full reset of Docker environment
echo ========================================

echo.
echo [1/5] Stopping and removing containers...
docker stop credit-scoring-api 2>nul
if %errorlevel% equ 0 (
    echo ✅ Stopped credit-scoring-api
) else (
    echo ℹ️  credit-scoring-api was not running
)

docker rm credit-scoring-api 2>nul
if %errorlevel% equ 0 (
    echo ✅ Removed credit-scoring-api
) else (
    echo ℹ️  credit-scoring-api container not found
)

docker stop credit-scoring-debug 2>nul
docker rm credit-scoring-debug 2>nul

echo.
echo [2/5] Removing images...
docker rmi credit-scoring-model 2>nul
if %errorlevel% equ 0 (
    echo ✅ Removed credit-scoring-model image
) else (
    echo ℹ️  credit-scoring-model image not found
)

echo.
echo [3/5] Cleaning up Docker system...
docker system prune -f

echo.
echo [4/5] Checking Docker status...
docker --version
if %errorlevel% equ 0 (
    echo ✅ Docker is available
) else (
    echo ❌ Docker is not available!
    goto error
)

echo.
echo [5/5] Verifying cleanup...
echo Current containers:
docker ps -a --filter "name=credit-scoring" --format "table {{.Names}}\t{{.Status}}"

echo.
echo Current images:
docker images --filter "reference=credit-scoring*" --format "table {{.Repository}}\t{{.Tag}}"

echo.
echo ========================================
echo ✅ Cleanup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. scripts\build.bat    - Build the Docker image
echo 2. scripts\run.bat      - Run the container
echo 3. scripts\logs.bat     - View logs
echo.
goto end

:error
echo.
echo ❌ There was an error during cleanup!
echo Please check that Docker is installed and running.
echo.

:end
pause