FROM python:3.10

RUN mkdir -p /opt/azion

COPY requirements.txt /opt/azion/requirements.txt
COPY src/main.py /opt/azion/main.py

WORKDIR /opt/azion

RUN pip install -r requirements.txt

ENTRYPOINT ["/opt/azion/main.py"]
