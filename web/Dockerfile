FROM alpine:latest

COPY requirements.txt wsgi.py /server/

RUN apk --no-cache add \
    python3 \
    py-gunicorn \
  && apk --update add --virtual build-dependencies gcc python-dev python3-dev libffi-dev build-base git postgresql-dev \
  && pip3 install -r /server/requirements.txt \
  && apk del build-dependencies \
  && adduser -D app \
  && mkdir -p /server  \
  && chown -R app:app /server

COPY server /server/server/

VOLUME /tmp

RUN chown -R app:app /server

WORKDIR /server

USER app

EXPOSE 8000

CMD ["/usr/bin/gunicorn", "-w 2", "-b :8000", "wsgi:app"]
