@echo off
echo ========================================
echo Starting Credit Scoring Model API (Fixed)
echo ========================================

echo Stopping existing container if running...
docker stop credit-scoring-api 2>nul
docker rm credit-scoring-api 2>nul

echo.
echo Starting new container with explicit settings...
docker run -d ^
  -p 8000:8000 ^
  --name credit-scoring-api ^
  --restart unless-stopped ^
  credit-scoring-model:latest

timeout /t 5 /nobreak >nul

echo.
echo Checking container status...
docker ps --filter "name=credit-scoring-api" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
if errorlevel 1 (
    echo ❌ Container failed to start!
    echo.
    echo Checking logs...
    docker logs credit-scoring-api 2>nul || echo "No logs available"
) else (
    echo ✅ Container started successfully!
    echo.
    echo 📍 API: http://localhost:8000
    echo 📚 Docs: http://localhost:8000/docs
    echo 🏥 Health: http://localhost:8000/health
)

echo.
pause