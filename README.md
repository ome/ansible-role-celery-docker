Celery Docker
=============

Celery distributed processing with Docker.
This role is considered developmental.


Dependencies
------------

See `meta/main.yml`

This role requires Docker to be running on the target hosts.
Celery requires a broker such as Redis, either on the current or a remote server.

For example, you can use the `openmicroscopy.docker` and `openmicroscopy.redis` roles to set them up, see the example playbook.


Variables
---------

All variables are optional:
- `celery_docker_broker_url`: The URL to the broker, e.g. `redis://HOST:PORT/DB`, default is redis on localhost
- `celery_docker_log_level`: Celery worker log level, default `DEBUG`
- `celery_docker_concurrency`: Number of concurrent tasks, default is number of CPUs
- `celery_docker_opts`: Additional options for celery worker
- `celery_docker_max_retries`: Maximum number of times to retry if the `docker` command fails, default `3`
- `celery_docker_retry_delay`: Delay (seconds) before retrying a failed task, default `10`
- `celery_docker_store_tasks_hours`: Store completed tasks in the broker for this number of hours, default `384` (16 days)
- `celery_docker_systemd_timeout`: If a Celery worker is stopped with `systemctl stop celery-worker` wait this number of seconds before killing the worker (this will kill any tasks still in progress), default `7200` (2 hours)


Usage
-----

This role creates a celery worker that launches docker containers.
At present a single task is defined, `run_docker`.
See [celery-worker-tasks.py `run_docker`](files/celery-worker-tasks.py) for a description of the parameters.

Tasks can be submitted in two ways:

- Submit a `run_docker` task with arguments passed as a dictionary.
  For an example of this see [celery-submit-example.py](files/celery-submit-example.py).

- Run the [tasks file](files/celery-worker-tasks.py) directly (a `main` function is included):

        /opt/celery/venv/bin/python /opt/celery/worker/tasks.py --help

        /opt/celery/venv/bin/python /opt/celery/worker/tasks.py
          --inputpath /celery/in --outputpath /celery/out --out /celery/output.log
          busybox -- sh -c 'date > /output/date.txt'


Example playbook
----------------

    - hosts: localhost
      roles:
      - role: openmicroscopy.docker
      - role: openmicroscopy.redis
      - role: celery-docker


Advanced setup
--------------

### Redis security

You can set a [password and other configuration options](http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html) when starting Redis (`--requirepass`), or in the Redis configuration file.
All communication is in plain text so this does not guard against network sniffing.
Redis can [write its data to disk](http://redis.io/topics/persistence) and reload it on startup (`--appendonly yes`) instead of running as an in-memory database.
For example, if you are running Redis in Docker:

    docker run -d --name redis -p 6379:6379 -v redis-volume:/data redis \
        --requirepass PASSWORD --appendonly yes

And set `celery_docker_broker_url: redis://:PASSWORD@redis.example.org:6379`


### Long-running tasks

The default Celery configuration is designed for handling short tasks.
There are several changes that can be made to improve the processing of long-running tasks, see the [configuration](http://docs.celeryproject.org/en/latest/configuration.html) and [optimising](http://docs.celeryproject.org/en/latest/userguide/optimizing.html) docs.

For example, use the `-Ofair` option `celery_docker_opts: -Ofair`


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
