FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip3 install -r requirements.txt

ENV PORT 5000

CMD gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
