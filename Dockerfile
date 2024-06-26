FROM python:3.6-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Add source code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "main.py", "--port", "5000"]
