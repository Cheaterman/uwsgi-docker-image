uWSGI docker image
==================

Usage
=====

- You need a `requirements.txt` file at the root of your project folder - even if empty. You can also set an alternate path using the `REQUIREMENTS_FILE` environment variable.
- Mount your project folder as `/code` volume of this image.
- To specify where your WSGI application module lives, you should use the `WSGI_MODULE` environment variable. It defaults to `wsgi:app`, which will work if you have a WSGI callable named `app` inside a `wsgi.py` file in your `/code` folder.
- Finally, uWSGI runs on port 5000, so don't forget to publish this port to your host (or link to other dockers) as needed.

Basically:

```docker run --volume /path/to/your/code:/code -e WSGI_MODULE=yourmodule:yourapp -e REQUIREMENTS_FILE=path/to/your/requirements.txt -p 127.0.0.1:5000:5000 cheaterman/uwsgi```

See also: [Docker Hub repository](https://hub.docker.com/r/cheaterman/uwsgi/)
