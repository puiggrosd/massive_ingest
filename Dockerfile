# Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install siege and curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends siege curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

    
COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
