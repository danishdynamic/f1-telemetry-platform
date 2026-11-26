
# Start with a lightweight Python image.
FROM python:3.12-slim

# All backend files will live inside /app.
WORKDIR /app

# Install dependencies first so Docker can cache this layer.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy our FastAPI application into the container.
COPY app ./app

# FastAPI will listen on port 8000.
EXPOSE 8000

# Start the development server with automatic code reload.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
