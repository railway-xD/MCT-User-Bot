FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends git curl ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY . /app/
WORKDIR /app/

RUN pip3 install -U -r requirements.txt

CMD ["bash", "start.sh"]
