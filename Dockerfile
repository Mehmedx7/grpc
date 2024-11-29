FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y dos2unix

WORKDIR /app
COPY . .

ARG IS_IN_PRODUCTION

RUN pip install pip-tools \
    && pip install -r requirements.txt

CMD ["/bin/sh", "-c", "dos2unix /app/scripts/* && chmod +x /app/scripts/* && /app/scripts/start.sh"]