@echo off
echo Starting Credit Scoring Model API...

docker run -d -p 8000:8000 --name credit-scoring-api credit-scoring-model

echo Container started successfully!
echo API is available at: http://localhost:8000
echo Docs available at: http://localhost:8000/docs
echo To view logs: docker logs -f credit-scoring-api
echo To stop: docker stop credit-scoring-api
echo To remove: docker rm credit-scoring-api
pause