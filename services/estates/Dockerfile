FROM alpine:latest

RUN apk add --update python3 py3-pip gcc make py3-wheel python3-dev linux-headers musl-dev

EXPOSE 9009/tcp

COPY /app/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./app /app

WORKDIR /app

VOLUME /data

CMD ./app.py
