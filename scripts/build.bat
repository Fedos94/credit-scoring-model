@echo off
echo Building Credit Scoring Model Docker image...

docker build -t credit-scoring-model .

echo Build completed successfully!
echo You can run the container with: docker run -p 8000:8000 credit-scoring-model
pause