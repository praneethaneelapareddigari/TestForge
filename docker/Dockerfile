FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk maven golang-go nodejs npm git curl gcc \
  && rm -rf /var/lib/apt/lists/*

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Optionally install JS/TS tools globally for adapters (CI may prefer pinned install)
RUN npm install -g stryker-cli

ENTRYPOINT ["python", "-m", "testforge"]
