FROM python:3.8-alpine

RUN apk update && apk add gcc libc-dev libffi-dev

RUN adduser -D parthenopeddit

WORKDIR /home/parthenopeddit

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY parthenopeddit.py config.py cli.py mock_data.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP parthenopeddit.py

RUN chown -R parthenopeddit:parthenopeddit ./
USER parthenopeddit

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]