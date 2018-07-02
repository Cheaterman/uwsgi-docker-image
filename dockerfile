FROM gcr.io/google-appengine/python

RUN virtualenv -p $(which python3) /env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

RUN pip install uwsgi

ADD run.sh /run.sh

CMD []
ENTRYPOINT ["/run.sh"]
