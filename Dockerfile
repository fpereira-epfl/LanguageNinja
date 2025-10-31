FROM python:3.11-slim

# (Optional) faster builds for some wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code + static assets + data
COPY . .

# Expose the port
ENV PORT=8080

# Start the app (Gunicorn + Uvicorn worker)
CMD ["gunicorn", "-c", "gunicorn.conf.py", "languageninja.api.main:app"]