FROM python:3.6

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./ /

ENV AM_I_IN_A_DOCKER_CONTAINER Yes
ENV PYTHONUNBUFFERED 1

CMD python /src/api_main.py