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
SCRIPT_NAME = os.environ.get('SCRIPT_NAME', '/')

os.chdir('/code')

if os.environ.get('UPGRADE_REQUIREMENTS'):
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
    subprocess.run(['su', 'uwsgi'], check=True)

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

    wsgi_socket_gid = int(os.environ.get('WSGI_SOCKET_GID', gid))
    master_fifo_gid = int(os.environ.get('MASTER_FIFO_GID', gid))

    def chmod_master_fifo():
        while True:
            time.sleep(1)
            os.chown(master_fifo, uid, master_fifo_gid)
            os.chmod(master_fifo, 0o660)

    threading.Thread(target=chmod_master_fifo, daemon=True).start()

    with subprocess.Popen([
        'uwsgi',
        '--uid', 'uwsgi',
        '--gid', 'uwsgi',
        '--plugin', 'python',
        '--plugin', 'gevent',
        '--virtualenv', '/env',
        '--chdir', '/code',
        '--mount', f'{SCRIPT_NAME}={WSGI_MODULE}',
        '--uwsgi-socket', os.environ.get('ADDRESS', '/run/wsgi.sock'),
        '--chmod-socket=660',
        f'--chown-socket=uwsgi:{wsgi_socket_gid}',
        '--die-on-term',
        '--lazy-apps',
        '--master-fifo', master_fifo,
        '--workers', os.environ.get('WORKERS', '4'),
        '--listen', '1024',
        '--gevent', '1000',
        '--wsgi-disable-file-wrapper',
        '--ignore-sigpipe',
        '--ignore-write-errors',
        '--disable-write-exception',
        '--manage-script-name',
    ]) as uwsgi_process:
        def term_handler(*args):
            uwsgi_process.terminate()

        signal.signal(signal.SIGTERM, term_handler)
        uwsgi_process.wait()
