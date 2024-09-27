# Technical Test Template

## Quickstart

This is a modified version of the original skeleton template.

The only additions/changes are:

- user_monitoring/alert_controller.py
  - This file contains a class with static methods, used to check the transaction history against alerts
  - One might say the static methods are pure functions (they perform no IO, and mutate no variables outside the scope of the function). However, that's not really accurate as the functions mutate the variables they create.
- user_monitoring/mock_db.py
  - This file contains a class with a mock database, implemented as a Python dict
- user_monitoring/api.py
  - This file wasn't created by me, but I made small commented edits to it, integrating it with the two files I did create
- tests/api_test.py
  - I created 9 test cases that can be run with `make test`, just as with the original skeleton
  - I ask not to be penalised for the Ruff lint warnings in this file: I gave my explanation on why I thought it was a good reason to ignore them in the comments.

Since this repository is a modification of the original skeleton given, the running, testing, and installing commands are all the same and wholly unmodified.

