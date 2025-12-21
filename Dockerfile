# Стадия сборки зависимостей
FROM python:3.10-slim AS builder

# Установка системных зависимостей для ONNX Runtime
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Финальная стадия
FROM python:3.10-slim

# Системные зависимости в финальном образе
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости из стадии builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Копируем исходный код
COPY src/ ./src/

# Копируем ВСЕ файлы ONNX модели
COPY credit_model.onnx* ./

# Переменные окружения
ENV PYTHONPATH=/app/src
ENV MODEL_PATH=/app/credit_model.onnx

# Запуск приложения
EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]