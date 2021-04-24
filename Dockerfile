FROM python:3.8.2-slim as base

RUN apt-get update && apt-get install -y \
    g++ \
    make \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libmagic-dev \
    python3-matplotlib \
    python3-cryptography \
    libjpeg-dev \
    libfreetype6-dev \
    libopenjp2-7 \
    libtiff5 \
    zlib1g-dev \
    git \
    netcat \
    gcc

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /srv
RUN git clone https://github.com/matplotlib/matplotlib
RUN cd matplotlib && python setup.py build && python setup.py install

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

WORKDIR /app
COPY . .

EXPOSE $PORT

CMD ["sh", "-c", "python -m bot"]