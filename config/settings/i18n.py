# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

from django.utils.translation import gettext_lazy as _

from . import BASE_DIR

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Etc/UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Removed LANGUAGES list to support all languages
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr', _('Français (France)')),
# ]
