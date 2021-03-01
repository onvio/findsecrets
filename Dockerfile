FROM python:3.8.6-slim-buster

COPY . /opt/
WORKDIR /opt/
VOLUME /var/reports
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "/opt/findsecrets.py" ]