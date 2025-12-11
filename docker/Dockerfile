FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget supervisor tor && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/ /app/src
COPY scripts/ /app/scripts
COPY config/ /app/config
COPY static/ /app/static

RUN pip install --no-cache-dir -r /app/config/requirements.txt

RUN mkdir -p /var/lib/tor/hidden_service

ENV LLAMA_API_KEY=""
ENV LLAMA_API_URL="https://api.llama.com/v1/chat/completions"

EXPOSE 5000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]