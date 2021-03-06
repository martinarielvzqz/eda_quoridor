# EDA: Quoridor
Quoridor bot client for EDA

[![Build Status](https://app.travis-ci.com/martinarielvzqz/eda_quoridor.svg?token=Cn4W6Wq2fytkMsceRcpS&branch=main)](https://app.travis-ci.com/martinarielvzqz/eda_quoridor)

[![Coverage Status](https://coveralls.io/repos/github/martinarielvzqz/eda_quoridor/badge.svg)](https://coveralls.io/github/martinarielvzqz/eda_quoridor)

## Installation
clone and install dependencies

```sh
git clone https://github.com/martinarielvzqz/eda_quoridor.git
cd eda_quoridor
pipenv install
pipenv shell
pipenv install -r requirements.txt
pipenv install --dev -r requirements-dev.txt  # only required for run tests
```

## Configuration
```sh
cp env.sample .env
```
Configure your credentials in config.yml


## Run
```sh
python run.py
```


# Docker

```sh
docker build -t quoridor_client .
```

```sh
docker run --rm \
    --name quoridor_client \
    --mount type=bind,source=/var/log/quoridor,target=/usr/src/app/logs \
    quoridor_client
```
