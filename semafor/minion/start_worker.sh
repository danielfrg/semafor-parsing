#!bin/bash
USER=""
if id -u "vagrant" > /dev/null 2>&1; then
  USER="vagrant"
elif id -u "ubuntu" > /dev/null 2>&1; then
  USER="ubuntu"
else
  echo "No 'vagrant' or 'ubuntu' users found, stoping"
  exit 1
fi

if [ -e /home/$(echo $USER)/celery.pid ]
then
    kill -9 $(cat /home/$(echo $USER)/celery.pid)
fi
export PYTHONPATH=/home/$(echo $USER)/semafor/app:$PYTHONPATH

/home/$(echo $USER)/venv/bin/celery worker --app=semafor.minion.worker.celery -D -l info --concurrency=1 --queues=semafor.minion --logfile=/home/$(echo $USER)/celery.log --pidfile=/home/$(echo $USER)/celery.pid --broker=$1