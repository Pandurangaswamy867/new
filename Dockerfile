FROM python:3

# Set the working directory
WORKDIR /app

# Copy all application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS X-Ray daemon
RUN apt-get update && \
    apt-get install -y unzip && \
    curl -o /tmp/xray-daemon.deb https://s3.amazonaws.com/aws-xray-daemon/linux/latest/xray-daemon-3.x86_64.rpm && \
    dpkg -i /tmp/xray-daemon.deb

# Expose the ports for the application and X-Ray daemon
EXPOSE 2000 2000/udp

# Set environment variables for X-Ray
ENV AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000
ENV AWS_XRAY_CONTEXT_MISSING=LOG_ERROR

# Start X-Ray daemon in the background and run the Flask app
CMD ["/bin/sh", "-c", "xray -o & gunicorn -b 0.0.0.0:2000 app:app"]
