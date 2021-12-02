FROM python:3.9

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir -r requirements.txt

