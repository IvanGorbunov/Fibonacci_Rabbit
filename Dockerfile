FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /fibonacci

# install dependences
COPY ./requirements.txt /fibonacci/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /fibonacci/requirements.txt

