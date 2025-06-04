# 1. Base image: use Python 3.10 (slim variant)
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create and set workdir
WORKDIR /app

# 4. Install system dependencies (if any). For this simple example, none are strictly required.
#    But if you need e.g. libpq-dev or others, install here:
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements.txt and install Python dependencies
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt

# 6. Copy application code
COPY ./app /app

# 7. Expose port (optional, since docker-compose maps it)
EXPOSE 8000

# 8. Run Uvicorn server on container start
#    We bind to 0.0.0.0 so it is accessible from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
