FROM python:3.12

# 
WORKDIR /code

# 
COPY ./requirements.txt requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY ./src src

WORKDIR src
# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--loop", "asyncio"]
#
#docker run --name dlaibd -p 5432:5432 -e POSTGRES_USER=dlaibd -e POSTGRES_PASSWORD=dlaibd -e POSTGRES_DB=dlaibd -d postgres
#uvicorn main:app --host 127.0.0.1 --port 8000 --loop asyncio