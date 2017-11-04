FROM alpine:latest

COPY requirements.txt wsgi.py /server/

RUN apk --no-cache add \
    python \
    py-pip \
  && apk --update add --virtual build-dependencies gcc python-dev libffi-dev openssl-dev build-base git \
  && pip install -r /server/requirements.txt \
  && apk del build-dependencies \
  && adduser -D app \
  && mkdir -p /server  \
  && chown -R app:app /server

COPY server /server/server/

VOLUME /tmp

RUN chown -R app:app /server

WORKDIR /server

USER app

EXPOSE 8080

CMD ["python", "wsgi.py"]
