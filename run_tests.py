#!/usr/bin/env python

import os
import sys
import django
from django.conf import settings


def delete_migrations():
    from os.path import exists, abspath, dirname, join
    migrations_dir = join(
        dirname(abspath(__file__)), 'django_enumfield_named_choices', 'tests', 'migrations')
    if exists(migrations_dir):
        os.system('rm -r ' + migrations_dir)


def main():
    import warnings
    # Ignore deprecation warning caused by Django on 3.7 + 2.0
    is_py37_django20 = (
        sys.version_info[:2] == (3, 7) and django.VERSION[:2] == (2, 0)
    )
    module = r"(?!django).*" if is_py37_django20 else ""
    warnings.filterwarnings('error', module=module, category=DeprecationWarning)

    delete_migrations()

    if not settings.configured:
        # Dynamically configure the Django settings with the minimum necessary to
        # get Django running tests
        settings.configure(
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
                        
    'django_enumfield_named_choices',
],

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django_applog.AppLogMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
),
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
],

#            INSTALLED_APPS=[
#                'django.contrib.auth',
#                'django.contrib.contenttypes',
#                'django.contrib.admin',
#                'django.contrib.sessions',
#                'django_enumfield_named_choices',
#                'django_enumfield_named_choices.tests',
#            ],
            # Django replaces this, but it still wants it. *shrugs*
            DATABASE_ENGINE='django.db.backends.sqlite3',
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                }
            },
            MEDIA_ROOT='/tmp/django_enums/',
            MEDIA_PATH='/media/',
            ROOT_URLCONF='django_enumfield_named_choices.tests.urls',
            DEBUG=True,
            TEMPLATE_DEBUG=True,
        )

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    if '--failfast' in sys.argv:
        test_runner.failfast = True

    failures = test_runner.run_tests(['django_enumfield_named_choices'])

    delete_migrations()

    sys.exit(failures)


if __name__ == '__main__':
    main()
