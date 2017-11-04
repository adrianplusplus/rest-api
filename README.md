# Tourister Backend

[![Build Status](https://travis-ci.org/TODO?branch=master)](https://travis-ci.org/TODO)

## Quick Start

Contains the flask backend with JWT authentication methods and a GraphQL API

### Basics

1. Create and activate a virtualenv

```bash
# install virtualenv globally
pip install virtualenv

#create virtualenv
virtualenv env

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
$ export APP_SETTINGS="server.config.DevelopmentConfig"
```

or

```bash
$ export APP_SETTINGS="server.config.ProductionConfig"
```

### Create DB

```bash
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
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
