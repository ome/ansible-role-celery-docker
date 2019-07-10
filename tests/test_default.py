import testinfra.utils.ansible_runner
import pytest
from time import sleep

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize("name", [
    "celery-worker",
    "docker",
    "redis",
])
def test_services_running_and_enabled(Service, name):
    assert Service(name).is_running
    assert Service(name).is_enabled

@pytest.mark.skip(reason="needs to be reviewed")
def test_celery_task(Command, File, Sudo):
    with Sudo():
        Command.check_output(
            'rm -f /tmp/celery/output.txt /tmp/celery/log.out')

    taskid = Command.check_output(
        '/opt/celery/venv/bin/python %s %s %s %s %s %s %s %s %s %s %s %s',
        '/opt/celery/worker/tasks.py',
        '--inputpath', '/tmp/celery/input.txt',
        '--outputpath', '/tmp/celery',
        '--out', '/tmp/celery/log.out',
        'busybox', '--',
        'sh', '-c',
        'md5sum /input > /output/output.txt && echo Done'
    )
    assert taskid

    # WARNING: If the network is particularly slow the download of busybox
    # may take too long
    for i in xrange(20):
        got_outputs = (File('/tmp/celery/log.out').exists and
                       File('/tmp/celery/output.txt').exists)
        # Sleep first to allow time for writing
        sleep(10)
        if got_outputs:
            break

    flog = File('/tmp/celery/log.out')
    assert flog.exists
    assert flog.content_string.strip() == 'Done'

    fout = File('/tmp/celery/output.txt')
    assert fout.exists
    assert fout.content_string.strip() == \
        '5eb63bbbe01eeed093cb22bb8f5acdc3  /input'
