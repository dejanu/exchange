FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Expose Flask default port
EXPOSE 5000

# Default command: run web interface
CMD ["python", "web.py"]
