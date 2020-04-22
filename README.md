uWSGI docker image
==================

Usage
=====

- You need a `requirements.txt` file at the root of your project folder - even if empty. You can also set an alternate path using the `REQUIREMENTS_FILE` environment variable.
- Mount your project folder as `/code` volume of this image.
- To specify where your WSGI application module lives, you should use the `WSGI_MODULE` environment variable. It defaults to `app:app`, which will work if you have a WSGI callable named `app` inside a `app.py` file in your `/code` folder.
- Finally, by default, uWSGI listens on a UNIX socket named `wsgi.sock` that will be placed in a newly-created `run/` directory in your project folder (mounted to `/run` inside the image). You should point your production webserver to this socket in order to serve your application. You can also affect this behavior using the `ADDRESS` environment variable - set it to any other UNIX socket path (default `/run/wsgi.sock`) or even to a TCP host/port (eg. `127.0.0.1:5000`).

Basically:

```
docker run \
    -v /path/to/your/code:/code \
    -e WSGI_MODULE=yourmodule:yourapp \
    -e REQUIREMENTS_FILE=/path/to/your/code/requirements.txt \
    cheaterman/uwsgi
```

See also: [Docker Hub repository](https://hub.docker.com/r/cheaterman/uwsgi/)
