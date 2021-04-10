FROM python:3.8.2-slim as base

RUN apt-get update && apt-get install -y \
    libpq-dev \
    libffi-dev \
    libmagic-dev \
    python3-matplotlib \
    python3-cryptography \
    netcat \
    gcc

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY . .

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN poetry export > requirements.txt
RUN pip install -r requirements.txt --no-deps

EXPOSE $PORT

CMD ["sh", "-c", "python -m bot"]