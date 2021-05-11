FROM python:3.7

RUN pip install Flask gunicorn requests_toolbelt sseclient python_jwt numpy pandas

COPY . app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 app:app

