FROM python:latest

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    openjdk-17-jdk \
    wget \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

RUN wget -qO- https://get.nextflow.io | bash && \
    mv nextflow /usr/local/bin/ && \
    chmod +x /usr/local/bin/nextflow
# soporte completo para WebSocket
RUN pip install "uvicorn[standard]"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
