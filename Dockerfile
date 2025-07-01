# FROM python:3.7-slim-buster

# EXPOSE 8501

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY . /app

# RUN pip3 install -r requirements.txt

# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


# Use Python 3.10 to satisfy altair version requirement
FROM python:3.10-slim

EXPOSE 8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
