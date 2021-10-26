FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1

ARG USER_UID
ARG USER_GID

# RUN addgroup --gid $USER_GID django && adduser --disabled-password --gecos "" --ingroup django --uid "$USER_UID" django #alpine

# RUN useradd -r -u $USER_UID -g root django # ubuntu/centos

# Debian
RUN addgroup --gid $USER_GID django && adduser --uid $USER_UID --gid $USER_GID --disabled-password django

# USER django

RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/

# alpine install psycopg2
#RUN apk add --no-cache --virtual .build-deps \
#    gcc \
#    python3-dev \
#    musl-dev \
#    postgresql-dev \
#    && pip install --no-cache-dir psycopg2 \
#    && apk del --no-cache .build-deps

RUN pip install -r requirements.txt

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
# RUN chown -R django:django /usr/local/lib/node_modules

RUN chown -R django:django /home/django
RUN chown -R django:django /code
# RUN chown -R django:django /home/django/.config
USER django

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]