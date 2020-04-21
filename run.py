#!/usr/bin/env python3
import contextlib
import grp
import os
import pwd
import subprocess
import sys
import threading
import time


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
        time.sleep(1)
        os.chmod(master_fifo, 0o666)

    threading.Thread(target=chmod_master_fifo).start()

    subprocess.run([
        'uwsgi',
        '--uid', 'uwsgi',
        '--gid', 'uwsgi',
        '--plugin', 'python',
        '--plugin', 'gevent',
        '--virtualenv', '/env',
        '--chdir', '/code',
        '-w', os.environ.get('WSGI_MODULE', 'app:app'),
        '--uwsgi-socket', os.environ.get('ADDRESS', '/run/wsgi.sock'),
        '--chmod-socket=666',
        '--lazy-apps',
        '--master-fifo', master_fifo,
        '--workers', os.environ.get('WORKERS', '4'),
        '--listen', '1024',
        '--gevent', '1000',
        '--gevent-monkey-patch',
        '--disable-logging',
    ])
