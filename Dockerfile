FROM python:3.10 as base

WORKDIR /home/starnavi

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt


# development image.
FROM base as development

COPY requirements_dev.txt requirements_dev.txt

RUN pip install -r requirements_dev.txt


# bot image.
FROM base as bot

COPY bot_requirements.txt bot_requirements.txt

RUN pip install --upgrade pip && pip install -r bot_requirements.txt
