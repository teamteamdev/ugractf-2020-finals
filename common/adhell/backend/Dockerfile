FROM python:3

COPY requirements.txt /

RUN pip3 install gunicorn -r /requirements.txt --no-cache-dir

COPY . /app
RUN cd app && python3 setup.py install

CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:80", "adhell.wsgi:app"]
