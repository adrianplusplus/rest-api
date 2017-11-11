# Tourister Service API

[![Build Status](https://TODO/TODO?branch=master)](https://TODO/TODO)

## Quick Start

Contains the flask backend with JWT authentication methods, and a REST API

### Dockerized Version

The current build is using `nginx` to serve static files.

1. In project root directory execute `docker build .`

2. Execute `docker run -p 5000:8080 <IMAGE ID>`

3. Navigate to `http://localhost:5000`

### Basics

1. Create and activate a virtualenv

```bash
#create virtualenv
python -m venv env

# activate:

# for linux
source env/bin/activate

# or, for windows
env/Scripts/activate
```

1. Install the requirements

```bash
# virtualenv must be active
pip install -r requirements.txt`
```

### Set Environment Variables

```bash
$ export FLASK_CONFIGURATION="server.config.DevelopmentConfig"
```

or

```bash
$ export FLASK_CONFIGURATION="server.config.ProductionConfig"
```

Set a SECRET_KEY

```sh
$ export SECRET_KEY="change_me"
```

### Create DB (Optional)

Create the databases in `psql`:

```sh
$ psql
# create database avante_service_api
# create database avante_service_api_test
# \q
```

### Create DB tables and run migrations (Optional)

```bash
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
```

### Run the Application

```bash
$ python manage.py runserver
```

So access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```bash
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```bash
$ python manage.py test
```

With coverage:

```bash
$ python manage.py cov
```
