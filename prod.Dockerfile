FROM python:3.12.7

WORKDIR /app

COPY ./prod.requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

ENTRYPOINT ["/app/entrypoint.sh"]
