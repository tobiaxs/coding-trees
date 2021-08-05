# Coding Trees

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
![Continuous Integration and Delivery](https://github.com/tobiwankenobii/coding-trees/workflows/Github%20Actions/badge.svg?branch=main)
[![Documentation Status](https://readthedocs.org/projects/coding-trees/badge/?version=latest)](https://coding-trees.readthedocs.io/en/latest/?badge=latest)

Django project for creating decision trees, which are meant to help programmers choose correct solution for their problems.

The inspiration for this project was a operator decision tree of [the RxJS library](https://rxjs.dev/operator-decision-tree).
My idea was to generalize this functionality, so that such trees could be created for each library or framework, or for general programming concepts, such as design patterns.

[**See the Coding Trees documentation for more information**](https://coding-trees.readthedocs.io/en/latest/).

## Getting started

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

You can also find useful commands in the `Makefile`.
