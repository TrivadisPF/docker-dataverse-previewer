#
#  Author: Guido Schmutz
#  Date: 2020-07-27
#
#  https://github.com/trivadispf/docker-presto-cli
#
# Use an official Python image as the base
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && \
    apt-get install -y curl tar && \
    rm -rf /var/lib/apt/lists/*

# Download and install wait4x
RUN curl -#LO https://github.com/atkrad/wait4x/releases/latest/download/wait4x-linux-amd64.tar.gz && \
    tar --one-top-level -xvf wait4x-linux-amd64.tar.gz && \
    cp ./wait4x-linux-amd64/wait4x /usr/local/bin/wait4x && \
    rm -rf wait4x-linux-amd64 wait4x-linux-amd64.tar.gz

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY entrypoint.sh /app/
COPY previewers.yaml /app/
COPY dataverse-cli.py /app/

# Define the command to run your CLI
ENTRYPOINT ["./entrypoint.sh"]