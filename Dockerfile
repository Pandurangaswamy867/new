# Use a lightweight Python image
FROM python:3.9.6-slim-buster

# Set the working directory
WORKDIR /app

# Copy application files
ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 2000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:2000", "app:app"]
