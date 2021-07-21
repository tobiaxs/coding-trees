# Django Light Boiler

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![Continuous Integration and Delivery](https://github.com/tobiwankenobii/django-light-boiler/workflows/Github%20Actions/badge.svg?branch=main)

Django projects starter which is meant to be easy to setup and use. It covers the most important topics like DRF, JWT support, Swagger docs and also technologies for local development, like docker, pre-commit and pytest. Boiler is prepared to work with the wemake-python-styleguide.

### Getting started

The local setup is made with docker-compose. Example and working `.env` file is in `docker` folder and it's connected
by default in compose file.

Building the images

```shell
docker-compose build
```

Running the containers

```shell
docker-compose up
```
