from __future__ import absolute_import

from celery import Celery

app = Celery()

app.config_from_object('semafor.minion.worker.celeryconfig')
