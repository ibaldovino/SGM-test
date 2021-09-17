FROM python:3.8
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install gettext -y

COPY requirements.txt /tmp/
RUN pip install \
  --no-cache-dir \
  -r /tmp/requirements.txt


WORKDIR /app
COPY . /app

RUN chmod +x docker-entrypoint.sh