FROM python:3.11

WORKDIR /code


COPY ./ /code
COPY prod.env ./.env

RUN pip install --no-cache-dir -r requirements.txt
