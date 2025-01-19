FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app
ENTRYPOINT [ "python3", "-u", "main.py" ]