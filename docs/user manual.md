# User Manual
|Author|魏子軒|Date|2021-10-14|
|-|-|-|-|

## Installing packages in the first time

1. execute following commands
    ```shell
    cd /path/to/src
    pipenv install --dev
    ```

## Run Server

### On host environment
1. execute following commands
    ```shell
    cd /path/to/src
    pipenv run python start.py
    ```
2. server runs on http://127.0.0.1:58080

### On docker
1. execute following commands
    ```shell
    cd /path/to/src
    docker-compose up --build tasklist
    ```
2. server runs on http://127.0.0.1:58080

## Run Test

### On host environment
1. execute following commands
    ```shell
    cd /path/to/src
    pipenv run pytest -s -vv tests/
    ```
2. wait until test finishes

### On docker
1. execute following commands
    ```shell
    cd /path/to/src
    docker-compose up --build tasklist-unit-test
    ```
2. wait until test finishes

## Web APIs

Please reference section **Web APIs** in document **design**