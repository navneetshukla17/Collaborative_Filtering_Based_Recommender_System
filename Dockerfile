FROM python:3.10-slim

EXPOSE 8080

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Correct way: Use CMD instead of ENTRYPOINT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
