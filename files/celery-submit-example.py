#!/usr/bin/env python
# Example standalone Python script for submitting tasks to celery by passing
# parameters as keywords only. You do not need access to the original app
# (tasks.py) file.

from celery import Celery

CELERY_BROKER = 'redis://'

celery = Celery(broker=CELERY_BROKER)
celery_docker_args = dict(
    image='manics/pyfeatures:merge',
    command='calc /input/image1.avro --out-dir /output/image1 ',
    # Must be writeable by celery:
    logoutfile='/features/logs/log.txt',
    # Mounted inside container as /input (read-only):
    inputpath='/features/input',
    # Mounted inside container as /output:
    outputpath='/features/output',
    user='1000',
)
taskid = celery.send_task('tasks.run_docker', kwargs=celery_docker_args)
print taskid
