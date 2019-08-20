django-enumfield-named-choices-named-choices
===============================

Provides an enumeration Django model field (using IntegerField) with reusable enums and transition validation.

.. image:: https://img.shields.io/pypi/v/django-enumfield-named-choices.svg
    :target: https://pypi.python.org/pypi/django-enumfield-named-choices

.. image:: https://img.shields.io/pypi/l/django-enumfield-named-choices.svg
    :target: https://pypi.python.org/pypi/django-enumfield-named-choices

.. image:: https://img.shields.io/pypi/pyversions/django-enumfield-named-choices.svg
    :target: https://pypi.python.org/pypi/django-enumfield-named-choices

.. image:: https://img.shields.io/pypi/wheel/django-enumfield-named-choices.svg
    :target: https://pypi.python.org/pypi/django-enumfield-named-choices


Installation
------------

Install ``django-enumfield-named-choices`` in your Python environment:

.. code:: sh

    $ pip install django-enumfield-named-choices


Usage
-----

Create an Enum-class and pass it as first argument to the Django model EnumField.

.. code:: python

    from django.db import models
    from django_enumfield_named_choices import enum

    class BeerStyle(enum.Enum):
        LAGER = 0
        STOUT = 1
        WEISSBIER = 2

    class Beer(models.Model):
        style = enum.EnumField(BeerStyle, default=BeerStyle.LAGER)

.. code:: python

    Beer.objects.create(style=BeerStyle.STOUT)
    Beer.objects.filter(style=BeerStyle.STOUT)

You can use your own labels for Enum items

.. code:: python

    class Animals(enum.Enum):
        CAT = 1
        DOG = 2

        labels = {
            CAT: 'Cat',
            DOG: 'Dog'
        }

The Enum-class provides the possibility to use transition validation.

.. code:: python

    from django.db import models
    from django_enumfield_named_choices import enum

    class PersonStatus(enum.Enum):
        ALIVE = 1
        DEAD = 2
        REANIMATED = 3

        _transitions = {
            DEAD: (ALIVE,),
            REANIMATED: (DEAD,)
        }

    class Person(models.Model):
        status = enum.EnumField(PersonStatus)

These transitions state that a PersonStatus can only go to DEAD from ALIVE and to REANIMATED from DEAD.

.. code:: python

    person = Person.objects.create(status=PersonStatus.ALIVE)
    try:
        person.status = PersonStatus.REANIMATED
        person.save()
    except InvalidStatusOperationError:
        print("Person status can not go from ALIVE to REANIMATED")

The Enum-class can also be used without the EnumField. This is very useful in Django form ChoiceFields.

.. code:: python

    from django.forms import Form
    from django_enumfield_named_choices import enum

    class GenderEnum(enum.Enum):
        MALE = 1
        FEMALE = 2

        labels = {
            MALE: 'Male',
            FEMALE: 'Female',
        }

    class PersonForm(forms.Form)
        gender = forms.TypedChoiceField(choices=GenderEnum.choices(), coerce=int)

Rendering PersonForm in a template will generate a select-box with "Male" and "Female" as option labels for the gender field.
