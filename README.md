# NYU DevOps Project Template

[![Build Status](https://github.com/CSCI-GA-2820-SP24-001/customers/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-001/customers/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP24-001/customers/branch/master/graph/badge.svg?token=y6OUlCB4bC)](https://codecov.io/gh/CSCI-GA-2820-SP24-001/customers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a customer servivce for the Sprint 2024 DevOps

## Intro
One of my favorite quotes is:

_“If it's worth building, it's worth testing.
If it's not worth testing, why are you wasting your time working on it?”_

As Software Engineers we need to have the discipline to ensure that our code works as expected and continues to do so regardless of any changes, refactoring, or the introduction of new functionality.

You can read more about my thoughts on TDD in the article: [A Case for Test Driven Development](https://johnrofrano.medium.com/a-case-for-test-driven-development-7d9a552e0a16)

This lab introduces **Test Driven Development** using `PyUnit` and `PyTest`. It also demonstrates how to create a simple RESTful service using Python Flask and PostgreSQL. The resource model is persistence using SQLAlchemy to keep the application simple. It's purpose is to show the correct API calls and return codes that should be used for a REST API.

**Note:** The base service code is contained in `routes.py` while the business logic for manipulating Customers is in the `models.py` file. This follows the popular Model View Controller (MVC) separation of duties by keeping the model separate from the controller. As such, we have two test suites: one for the model (`test_models.py`) and one for the service itself (`test_routes.py`)

## Prerequisite Software Installation

This lab uses Docker and Visual Studio Code with the Remote Containers extension to provide a consistent repeatable disposable development environment for all of the labs in this course.

You will need the following software installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com)
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension from the Visual Studio Marketplace

All of these can be installed manually by clicking on the links above or you can use a package manager like **Homebrew** on Mac of **Chocolatey** on Windows.

Alternately, you can use [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) to create a consistent development environment in a virtual machine (VM). 

You can read more about creating these environments in my article: [Creating Reproducible Development Environments](https://johnrofrano.medium.com/creating-reproducible-development-environments-fac8d6471f35)

# Bring up the development environment

To bring up the development environment you should clone this repo, change into the repo directory:

```bash
git clone https://github.com/CSCI-GA-2820-SP24-001/customers.git
cd customers
```

Depending on which development environment you created, pick from the following:

### Start developing with Visual Studio Code and Docker

Open Visual Studio Code using the `code .` command. VS Code will prompt you to reopen in a container and you should say **yes**. This will take a while as it builds the Docker image and creates a container from it to develop in.

```bash
code .
```

Note that there is a period `.` after the `code` command. This tells Visual Studio Code to open the editor and load the current folder of files.

Once the environment is loaded you should be placed at a `bash` prompt in the `/app` folder inside of the development container. This folder is mounted to the current working directory of your repository on your computer. This means that any file you edit while inside of the `/app` folder in the container is actually being edited on your computer. You can then commit your changes to `git` from either inside or outside of the container.

### Using Vagrant and VirtualBox

Bring up the virtual machine using Vagrant.

```shell
vagrant up
vagrant ssh
cd /vagrant
```

This will place you in the virtual machine in the `/vagrant` folder which has been shared with your computer so that your source files can be edited outside of the VM and run inside of the VM.


## Running the tests

As developers we always want to run the tests before we change any code. That way we know if we broke the code or if someone before us did. Always run the test cases first!

Run the unit tests using `pytest`

```shell
make test
```

PyTest is configured via the included `setup.cfg` file to automatically include the `--pspec` flag so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

PyTest is also configured to automatically run the `coverage` tool and you should see a percentage-of-coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
coverage report -m
```

This is particularly useful because it reports the line numbers for the code that have not been covered so you know which lines you want to target with new test cases to get higher code coverage.

You can also manually run `pytest` with `coverage` (but settings in `pyporojrct.toml` do this already)

```shell
$ pytest --pspec --cov=service --cov-fail-under=95
```

Try and get as close to 100% coverage as you can.

It's also a good idea to make sure that your Python code follows the PEP8 standard. Both `flake8` and `pylint` have been included in the `pyproject.toml` file so that you can check if your code is compliant like this:

```shell
make lint
```

Which does the equivalent of these commands:

```shell
flake8 service tests --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics
pylint service tests --max-line-length=127
```

Visual Studio Code is configured to use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<customers>/
    cp .flaskenv ../<customers>/
    cp .gitattributes ../<customers>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## What's featured in the project?

- `service/__init__.py` -- establishes the Flask app factory
- `service/routes.py` -- the main Service routes using Python Flask
- `service/models.py` -- the data model using SQLAlchemy
- `tests/test_routes.py` -- test cases against the Customer service
- `tests/test_models.py` -- test cases against the Customer model

## Customer Service API Endpoints

This service provides a RESTful API for managing customers in the CustomerShop inventory. Below are the available endpoints along with their HTTP methods and brief descriptions:

# Health Check

GET /health
Provides a health check for the service, returning a 200 status code with a "Healthy" message if the service is up and running.

# Root URL

GET /
Serves the root URL response, ideally providing some useful information about the service in JSON format.

# Create a Customer

POST /customers
Creates a new customer with details provided in the request body in JSON format. Returns the created customer's details along with a 201 status code.

# Read a Customer

GET /customers/<int:customer_id>
Retrieves a single customer's details by their ID. Returns a 200 status code with the customer's details in JSON format if found, or a 404 if the customer is not found.

# Update a Customer

PUT /customers/<int:customer_id>
Updates an existing customer's details with the information provided in the request body in JSON format. The customer is identified by their ID. Returns the updated customer's details with a 200 status code if successful, or a 404 if the customer is not found.

# Delete a Customer

DELETE /customers/<int:customer_id>
Deletes a customer identified by their ID. Returns a 204 status code if the deletion is successful, indicating no content in the response.

# List All Customers

GET /customers
Retrieves a list of all customers. Supports query parameters for filtering by category or name. Returns a 200 status code with a list of customers matching the criteria, or all customers if no filters are applied.

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
