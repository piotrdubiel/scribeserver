FROM python:2.7.9

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y gfortran
RUN apt-get install -y libatlas-base-dev

RUN mkdir -p /code
WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 5000
CMD python server.py
