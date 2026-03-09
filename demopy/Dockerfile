FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only runtime source files
COPY web.py ./
COPY order.py ./
COPY orderbook.py ./
COPY price.py ./
COPY matchingengine.py ./
COPY templates ./templates

# Expose Flask default port
EXPOSE 5000

# Default command: run web interface
CMD ["python", "web.py"]
