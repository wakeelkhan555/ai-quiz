# Use an official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from creating cache files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python output immediately
ENV PYTHONUNBUFFERED=1

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY server.py .
COPY question.json .
COPY frontend/ ./frontend/

# Expose the FastAPI port
EXPOSE 8000

# Start the web server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
