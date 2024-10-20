FROM python:3.12.2
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
