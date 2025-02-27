FROM python:3

# Set the working directory
WORKDIR /app

# Copy all application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt #hlo##

# Expose the port that the app runs on
EXPOSE 2000

# Command to start the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:2000", "app:app"]
