FROM python:3.9-slim-buster

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/src/desire/chview

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/desire/chview/requirements.txt
RUN pip install -U pip --no-cache-dir && \
	pip install --no-cache-dir wheel && \
	pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh /usr/src/desire/chview/entrypoint.sh
COPY . /usr/src/desire/chview

ENTRYPOINT ["/usr/src/desire/chview/entrypoint.sh"]