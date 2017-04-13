Celery Docker
=============

Celery distributed processing with Docker.


Dependencies
------------

See `meta/main.yml`

This role requires Docker to be running on the target hosts.
Celery requires a broker such as Redis, either on the current or a remote server.

For example, you can use the `openmicroscopy.docker` and `openmicroscopy.redis` roles to set them up, see the example playbook.


Usage
-----

This role creates a celery worker that launches docker containers.
At present a single task is defined, `run_docker`.
See [celery-worker-tasks.py `run_docker`](files/celery-worker-tasks.py) for a description of the parameters.

Tasks can be submitted in two ways:

- Submit a `run_docker` task with arguments passed as a dictionary.
  For an example of this see [celery-submit-example.py](files/celery-submit-example.py).

- Run the tasks file directly (a `main` function is included):

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


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
