FROM alpine

RUN \
    apk add \
        python3 \
        uwsgi \
        uwsgi-python3 \
        uwsgi-gevent \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        file \
        make \
        shadow \
        && \
    mkdir /env && \
    usermod -d / -s /bin/sh uwsgi && \
    chown uwsgi: /env && \
    su uwsgi -c $' \
        python3 -m venv /env && \
        source /env/bin/activate && \
        pip3 install --no-cache-dir gevent \
    ' && \
    apk del \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        file \
        make \
        shadow

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD run.py /run.py

VOLUME /code /run

CMD []
ENTRYPOINT ["/run.py"]
