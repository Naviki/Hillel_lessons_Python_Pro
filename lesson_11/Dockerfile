FROM python:3.10

ENV DockerHOME=/home/ithillel/lesson_11/mono
ENV DB_HOST="host.docker.internal"

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . $DockerHOME
WORKDIR $DockerHOME/mono

RUN pipenv install

EXPOSE 8000

CMD pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8000