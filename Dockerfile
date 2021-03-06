# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "run_spider.py"]
