#!/usr/bin/env python3
import grp
import os
import pwd
import signal
import subprocess
import sys
import threading
import time


WSGI_MODULE = os.environ.get('WSGI_MODULE', 'app:app')

os.chdir('/code')
subprocess.run([
    'su',
    'uwsgi',
    '-c',
    ' '.join((
        'pip',
        'install',
        '--no-cache-dir',
        '--upgrade',
        '--requirement',
        os.environ.get('REQUIREMENTS_FILE', 'requirements.txt'),
    )),
], check=True)


if len(sys.argv) > 1 and sys.argv[1] == 'sh':
    subprocess.run(['su', 'uwsgi'])

else:
    uid, gid = (
        pwd.getpwnam('uwsgi').pw_uid,
        grp.getgrnam('uwsgi').gr_gid,
    )
    os.chown('/run', uid, gid)

    master_fifo = '/run/uwsgi.fifo'

    try:
        os.mkfifo(master_fifo)
    except FileExistsError:
        pass

    def chmod_master_fifo():
        while True:
            time.sleep(1)
            os.chmod(master_fifo, 0o666)

    threading.Thread(target=chmod_master_fifo, daemon=True).start()

    with subprocess.Popen([
        'uwsgi',
        '--uid', 'uwsgi',
        '--gid', 'uwsgi',
        '--plugin', 'python',
        '--plugin', 'gevent',
        '--virtualenv', '/env',
        '--chdir', '/code',
        '-w', WSGI_MODULE,
        '--uwsgi-socket', os.environ.get('ADDRESS', '/run/wsgi.sock'),
        '--chmod-socket=666',
        '--die-on-term',
        '--lazy-apps',
        '--master-fifo', master_fifo,
        '--workers', os.environ.get('WORKERS', '4'),
        '--listen', '1024',
        '--gevent', '1000',
        '--gevent-monkey-patch',
        '--disable-logging',
    ]) as uwsgi_process:
        def term_handler(*args):
            uwsgi_process.terminate()

        signal.signal(signal.SIGTERM, term_handler)
        uwsgi_process.wait()
