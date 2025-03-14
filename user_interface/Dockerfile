FROM python:3 AS stg1
COPY . .

RUN pip install --upgrade pip
RUN pip3 install cherrypy
# RUN apt install install sqlite3
# RUN pip3 install python-csv

FROM stg1
EXPOSE 9000

CMD [ "python3", "webserver_full.py"]
 