@echo off
echo Stopping Credit Scoring Model API...

docker stop credit-scoring-api 2>nul
docker rm credit-scoring-api 2>nul

echo ✅ Container stopped and removed

pause