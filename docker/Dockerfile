FROM python:3.11-slim

WORKDIR /app

# Copy app files
COPY src/app.py /app/
COPY index.html /app/
COPY manifest.json /app/
COPY requirements.txt /app/
COPY scripts/entrypoint.sh /app/scripts/

RUN chmod +x /app/scripts/entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt

ENV LLAMA_API_KEY=""

EXPOSE 5000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]