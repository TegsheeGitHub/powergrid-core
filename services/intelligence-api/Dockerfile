# -----------------------------------------------------------------------------
# PYTHON RUNTIME
# -----------------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# Prevent Python from writing pyc files and buffering stdout
# FIXED: Added "=" to satisfy Docker linting standards
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (none needed for this simple stack, but good practice)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application using Uvicorn (ASGI Server)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]