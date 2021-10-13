FROM python:3.9.7-buster as server
MAINTAINER Yuka <tzuhsuan@nature.ee.ncku.edu.tw>
EXPOSE 8080
COPY . /app
WORKDIR /app
RUN pip install pipenv &&\
    pipenv install
CMD pipenv run python start.py

FROM python:3.9.7-buster as unit-test
MAINTAINER Yuka <tzuhsuan@nature.ee.ncku.edu.tw>
EXPOSE 8080
COPY . /app
WORKDIR /app
RUN pip install pipenv &&\
    pipenv install --dev
CMD pipenv run pytest -s -vv tests/

