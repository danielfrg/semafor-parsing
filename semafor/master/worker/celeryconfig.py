BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_IMPORTS = ('semafor.master.worker.tasks', )

CELERY_ROUTES = {'semafor.master.worker.tasks.create_instances': {'queue': 'semafor.master'},
                 'semafor.master.worker.tasks.semafor_parse': {'queue': 'semafor.master'},}
