# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download & install AWS X-Ray daemon
RUN curl -o /usr/local/bin/xray-daemon https://s3.amazonaws.com/aws-xray-assets.us-east-1/xray-daemon-linux-3.x86_64 && \
    chmod +x /usr/local/bin/xray-daemon

# Expose necessary ports
EXPOSE 2000 2000/udp

# Start X-Ray Daemon and Gunicorn
CMD ["/usr/local/bin/xray-daemon", "-o", "127.0.0.1:2000", "--log-level", "debug"] & gunicorn -b 0.0.0.0:2000 app:app
