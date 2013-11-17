from __future__ import absolute_import

import os
from semafor.minion import settings
from semafor.minion import pipeline
from minion.worker.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def run_semafor(urls, readability_token, aws_key, aws_secret, s3_path,
                luigi_scheduler_host=''):
    import luigi
    
    # 0. Set settings
    settings.S3_PATH = s3_path
    settings.AWS_KEY = aws_key
    settings.AWS_SECRET = aws_secret
    settings.READABILITY_TOKEN = readability_token

    # 1. Create input file for pipeline
    fin = os.path.join(settings.DATA_DIR, settings.URLS_FILE)
    fin = open(fin, 'w')
    fin.write('\n'.join(urls))
    fin.close()

    # 2. Run pipeline
    args = ['--local-scheduler']
    if luigi_scheduler_host:
        args = ['--scheduler-host', luigi_scheduler_host]

    luigi.run(main_task_cls=pipeline.CopyToS3, cmdline_args=args)

    return 'OK'
