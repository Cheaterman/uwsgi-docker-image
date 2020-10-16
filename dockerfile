FROM alpine

RUN \
    apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        file \
        make \
        shadow \
        postgresql-dev \
        && \
    apk add --no-cache \
        python3 \
        uwsgi \
        uwsgi-python3 \
        uwsgi-gevent \
        tzdata \
        libpq \
        && \
    mkdir /env && \
    usermod -d / -s /bin/sh uwsgi && \
    chown uwsgi: /env && \
    su uwsgi -c $' \
        python3 -m venv /env && \
        source /env/bin/activate && \
        pip install --no-cache-dir -U pip && \
        pip install --no-cache-dir gevent==1.4.0 && \
        pip install --no-cache-dir psycopg2 \
    ' && \
    apk del --no-cache .build-deps

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD run.py /run.py

VOLUME /code /run

CMD []
ENTRYPOINT ["/run.py"]
