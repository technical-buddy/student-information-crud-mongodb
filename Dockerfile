# Docker Base Image >>
FROM python:3.10-slim

# Set Working Directory >> 
WORKDIR /app

# Copy All Code Files to Working Directory >>
COPY . /app

# Install Dependencies >>
RUN apt-get update && \
    apt install gnupg curl -y && \
    curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list && \
    apt-get update && \
    apt install -y mongodb-org && \
    pip install --no-cache-dir -r requirements.txt

# Create MongoDB data directory
RUN mkdir -p /data/db

# Expose Flask port >>
EXPOSE 5000
EXPOSE 27017

# Run Flask app >>
CMD mongod --dbpath /data/db --bind_ip 0.0.0.0 & python app.py