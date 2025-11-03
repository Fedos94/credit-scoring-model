@echo off
echo ========================================
echo Docker Container Status
echo ========================================

echo.
echo [Containers]
docker ps -a --filter "name=credit-scoring" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo [Images]
docker images --filter "reference=credit-scoring*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo.
echo [API Health Check]
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API is responding on http://localhost:8000/health
) else (
    echo ❌ API is not responding on port 8000
)

echo.
pause