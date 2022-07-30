FROM python:3.10.5-slim

# Make server directory and install os packages
RUN mkdir /server \
    && apt update \
    && apt install -y gcc
WORKDIR /server

# Copy poetry files
COPY ./server/pyproject.toml /server/
COPY ./server/poetry.lock /server/

# Install poetry and packages from pyproject.toml
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

# Copy code
COPY ./server /server
