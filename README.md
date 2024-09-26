# Technical Test Template

## Quickstart

This is a modified version of the original skeleton template.

The only three additions are:

- user_monitoring/alert_controller.py
  - This file contains a class with static methods, used to check the transaction history against alerts
  - One might say the static methods are pure functions (they perform no IO, and mutate no variables outside the scope of the function). However, that's not really accurate as the functions mutate the variables they create.
- user_monitoring/mock_db.py
  - This file contains a class with a mock database, implemented as a Python dict
- user_monitoring/api.py
  - This file wasn't created by me, but I made small commented edits to it, integrating it with the two files I did create

## Getting started

We have set up a basic Flask API that runs on port `5000` and included a `pytest` test showing the endpoint working.

If you prefer to use FastAPI, Django or other Python packages, feel free to add any you want using Poetry.
We have included a `Makefile` for conveince but you are free to run the project however you want.

### Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) for dependency management

### Install dependencies

```sh
poetry install
```

### Start API server

```sh
make run
```

### Run tests

```sh
make test
```

## Testing

```sh
curl -XPOST 'http://127.0.0.1:5000/event' -H 'Content-Type: application/json' \
-d '{ }'
```
