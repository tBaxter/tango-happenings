SECRET_KEY = "lorem ipsum"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tango_shared',
    'happenings',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'happenings.urls'
SITE_ID = 1

