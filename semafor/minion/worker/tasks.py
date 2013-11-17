from __future__ import absolute_import

import luigi
from minion import pipeline
from minion.worker.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def run_semafor(urls):
    '''
    '''
    # 1. Create input file for pipeline

    # 2. Run pipeline
    luigi.run(main_task_cls=pipeline.SemaforParsing)

    return 'OK'


