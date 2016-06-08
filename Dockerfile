FROM python:2
ADD . /code
WORKDIR /code
RUN python setup.py install
