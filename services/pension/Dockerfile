FROM python:3
RUN apt-get update && apt-get install -y build-essential
RUN wget https://deac-fra.dl.sourceforge.net/project/gnucobol/gnucobol/3.1/gnucobol-3.1-rc1.tar.xz && \
  tar -xaf gnucobol-3.1-rc1.tar.xz && \
  cd gnucobol-3.1-rc1 && \
  ./configure --prefix /usr && \
  make && make install
RUN pip3 install flask flask-wtf gunicorn filelock --no-cache-dir
COPY . /app
WORKDIR /app/core
RUN cobc -x -o /app/frontend/ADD-RETIREE ADD-RETIREE.COB && \
    cobc -x -o /app/frontend/ADD-PAYCHECK ADD-PAYCHECK.COB && \
    cobc -x -o /app/frontend/SHOW-PAYCHECKS SHOW-PAYCHECKS.COB && \
    cobc -x -o /app/frontend/CHANGE-PASSCODE CHANGE-PASSCODE.COB
WORKDIR /app/frontend
EXPOSE 8080
VOLUME /app/frontend/data
CMD gunicorn -b :8080 --workers=2 server:app
