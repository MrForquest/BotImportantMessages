FROM python:3.8.20-alpine3.20

WORKDIR /opt/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir  -r requirements.txt
COPY bot bot

ENTRYPOINT ["python", "bot/main.py"]