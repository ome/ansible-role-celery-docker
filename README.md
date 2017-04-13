Celery Docker
=============

Celery distributed processing with Docker.


Dependencies
------------

See `meta/main.yml`

Note that this uses `openmicroscopy.redis` by default.
If you have multiple redis users you may want to adjust the database used by each of them.


Usage
-----

This role creates a celery worker that launches docker containers.
For example, the following will submit a task:

    /opt/celery/venv/bin/python /opt/celery/worker/tasks.py
      --inputpath /celery/in --outputpath /celery/out --out /celery/output.log
      busybox -- sh -c 'date > /output/date.txt'

### Parameters
- `--inputpath /INPUT/PATH`: Input file or directory, mounted inside the Docker container as `/input`
- `--outputpath /OUTPUT/PATH`: Output file or directory, mounted inside the Docker container as `/output`.
  The user is responsible for ensuring it is writeable by the Docker container if necessary.

For more details run:

    /opt/celery/venv/bin/python /opt/celery/worker/tasks.py --help



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
