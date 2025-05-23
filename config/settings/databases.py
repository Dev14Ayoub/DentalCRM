import dj_database_url
from dotenv import load_dotenv

from .environment import BASE_DIR, DEBUG, LOCAL_RUN

load_dotenv()

if DEBUG and LOCAL_RUN:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    db_config = dj_database_url.config(conn_max_age=600, ssl_require=True)
    if not db_config:
        db_config = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    DATABASES = {
        'default': db_config
    }
