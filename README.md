# scheduler-web

[![Build Status](https://travis-ci.org/soldatov-ss/scheduler-web.svg?branch=master)](https://travis-ci.org/soldatov-ss/scheduler-web)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)


Python Environment Setup
1. Create and activate the virtual environment

```bash
uv venv
source .venv/bin/activate
```

2. Install all dependencies (including dev and lint tools)
```bash
 uv sync --all-groups
```

3. Start the dev server for local development:
```bash
docker-compose up --build
```