FROM python:3.10-buster 

RUN apt update && \
    apt install -y texlive-xetex texlive-fonts-recommended texlive-latex-recommended && \
    apt clean

# RUN useradd -s /bin/bash -m docmaker

# USER docmaker

ARG POETRY_VERSION="1.7.0"

RUN pip install poetry~=${POETRY_VERSION}

RUN poetry self add poetry-version-plugin

ENV POETRY_VIRTUALENVS_CREATE=false
