FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/raw data/processed models reports/figures

# Handle kaggle.json - copy if exists, skip if not
RUN if [ -f kaggle.json ]; then \
        mkdir -p /root/.kaggle && \
        cp kaggle.json /root/.kaggle/ && \
        chmod 600 /root/.kaggle/kaggle.json && \
        echo "Kaggle credentials copied"; \
    else \
        echo "No kaggle.json found, using kagglehub"; \
    fi

# Download data and train model
RUN python src/data/make_dataset.py
RUN python -c "from src.models.train_model import train_model; train_model()"

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]