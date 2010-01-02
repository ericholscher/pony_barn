import os
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = ( )

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

{% if db_engine %}
DATABASE_ENGINE = '{{ db_engine }}'
{% endif %}
{% if db_name %}
DATABASE_NAME = '{{ db_name }}'
{% endif %}
{% if db_pass %}
DATABASE_PASSWORD = '{{ db_pass }}'
{% endif %}
{% if db_user %}
DATABASE_USER = '{{ db_user }}'
{% endif %}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)

ROOT_URLCONF = 'urls'

{% if more_installed %}
INSTALLED_APPS += (
{% for app in more_installed %}
    '{{ app }}',
{% endfor %}
    )
{% endif %}
