import os
pid = os.getpid()

DATABASES = {
    'default': {
        'ENGINE': '{{ db_engine }}',
        'NAME': '{{ db_name }}',
        'USER': '{{ db_user}}',
        'PASSWORD': '{{ db_pass }}',
    },
    'other': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'other_db_%s' % pid,
    }
}
