FROM python:3.8-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install pipenv

COPY . /usr/src/app

RUN pipenv install --system --deploy --ignore-pipfile

CMD ['python', 'masque', '--dev']