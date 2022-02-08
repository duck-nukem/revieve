FROM python:3.10-alpine

RUN adduser --disabled-password worker
USER worker

RUN pip install --no-cache-dir --upgrade pip

COPY data /etc/data

COPY src /opt/app
WORKDIR /opt/app

CMD ["python", "main.py"]