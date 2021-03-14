## Promos API

REST API for promo system in which users are assigned various promos and can use the promo points in a specific task of
their choosing

[![Build Status](https://travis-ci.com/pnaoum/promos_api.svg?branch=master)](https://travis-ci.com/pnaoum/promos_api)
### Setup

1. Clone repo
2. Create virtual environment `venv` and work inside it
3. Install requirements using `pip install -r requirements.txt`
4. Create a `.env` file containing important app environment variables, on the same level as `manage.py`

Follow this template for `.env`

```bash
# General
# ------------------------------------------------------------------------------
SECRET_KEY=<my_secret_key>
DEBUG=False
ALLOWED_HOSTS=my,allowed,hosts

# Database
# ------------------------------------------------------------------------------
DATABASE_HOST=<db_hostname>
DATABASE_PORT=<db_port>
DATABASE_USER=<db_username>
DATABASE_PASSWORD=<db_password>
DATABASE_DB=<db_name>
DATABASE_ENGINE=django.db.backends.mysql
# Or use SQLite if needed
#DATABASE_ENGINE=django.db.backends.sqlite3
```

### Project Structure

```
promos_api/
│   config/ -> All app global configurations: settings - urls - wsgi - ..etc.
└───apps/
│   └───core   -> Contains core app views/models as health checks 
│   └───users  -> Contains Custom User models, authentication views
│   └───promos -> Contains promos models, views and urls 
└───swagger/ -> Configuration for swagger 
└───commons/ -> Global reusable utils for the app as pagination 
└───logs/ -> Contains log files for the configured loggers
└───requirements.txt -> All required python packages 
└───manage.py 
```

### Authentication

App uses token authentication, header `Authorization` with value `Token <my_token>` has to be provided with all requests

### Swagger

After running the project, swagger can be found at `/api/v1/swagger/`

To use different endpoints from swagger, signup with user, then login, copy the token returned and use `Authorize` on
the top right at the Swagger page, with the value `Token <my_token>`

### Admin

Admin is available in Debug mode only for the sake of manual testing, to change user roles at `/admin`