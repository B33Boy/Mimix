FROM python:3.11-slim

WORKDIR /workdir

RUN apt-get update \
    && apt-get install -y curl git vim \
    && rm -rf /var/lib/apt/lists/

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install ruff mypy python-dotenv