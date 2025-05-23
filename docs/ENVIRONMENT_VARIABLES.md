# Environment Variables Usage in DentalCRM

This document explains how environment variables are used in the DentalCRM project and how to set them up for local development and production.

## Overview

- The project uses environment variables to configure sensitive and environment-specific settings such as:
  - SECRET_KEY
  - DEBUG mode
  - ALLOWED_HOSTS
  - CSRF_TRUSTED_ORIGINS
  - Database connection URL
  - Email server settings
  - CORS allowed origins

- Environment variables are loaded in `config/settings/environment.py` using `python-dotenv`'s `load_dotenv()` function, which loads variables from a `.env` file in the project root during local development.

- Modular settings files like `databases.py`, `email.py`, and `cors_headers.py` also use environment variables for their configurations.

## Setting up Environment Variables

1. Create a `.env` file in the project root directory (same level as `manage.py`).

2. Add the necessary environment variables in the `.env` file. Example:

```
SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://localhost
DATABASE_URL=postgres://user:password@localhost:5432/dbname
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
CORS_ALLOWED_ORIGINS=https://localhost
```

3. Ensure `.env` is added to `.gitignore` to avoid committing sensitive information.

## Notes

- In production, set environment variables directly in the server environment instead of using a `.env` file.

- The project uses `dj_database_url` to parse the `DATABASE_URL` environment variable for database configuration.

- For any new settings that require environment-specific values, add them to `config/settings/environment.py` and use `os.environ.get()` with appropriate defaults.

## References

- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [dj-database-url](https://github.com/jacobian/dj-database-url)
- [Django deployment checklist](https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/)
