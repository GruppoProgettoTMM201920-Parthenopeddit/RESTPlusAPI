FROM python:3.8-alpine

RUN apk update && apk add --no-cache gcc libc-dev libffi-dev libressl-dev musl-dev libffi-dev openssl

WORKDIR /home/parthenopeddit

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY parthenopeddit.py config.py cli.py mock_data.py boot.sh ./
RUN chmod +x boot.sh

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]