FROM whmi/aiapi-web:latest AS aiapi-web

FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev nginx postgresql postgresql-contrib
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app
RUN pip install --default-timeout=100 -r requirements.txt

COPY --from=aiapi-web /app /usr/share/nginx/html

RUN service postgresql start && \
    su - postgres -c "psql -c \"CREATE USER myuser WITH PASSWORD 'mypassword';\"" && \
    su - postgres -c "psql -c \"CREATE DATABASE mydatabase WITH OWNER myuser;\""

EXPOSE 80 5432 8000

CMD ["sh", "-c", "service postgresql start && service nginx start && daphne -p 8000 -b 0.0.0.0 DjangoTest.asgi:application"]
