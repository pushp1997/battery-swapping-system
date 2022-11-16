FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update
RUN apt-get install netcat ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app/ /app/