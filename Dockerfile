FROM python:3.7

ADD . /group-i
WORKDIR /group-i

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
