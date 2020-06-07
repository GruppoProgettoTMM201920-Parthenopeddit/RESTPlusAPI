#!/bin/sh
# this script is used to boot a Docker container
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --certfile cert.pem --keyfile key.pem --worker-tmp-dir /dev/shm --access-logfile - --error-logfile - parthenopeddit:app