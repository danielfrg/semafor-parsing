CELERY_RESULT_BACKEND = 'amqp'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYD_PREFETCH_MULTIPLIER = 1

CELERY_IMPORTS = ('semafor.minion.worker.tasks', )

CELERY_ROUTES = {'semafor.minion.worker.tasks.run_semafor': {'queue': 'semafor.minion'}}