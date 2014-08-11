# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='tango-happenings',
    version='0.5.3',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    url='https://github.com/tBaxter/django-happenings',
    license='LICENSE',
    description='Reusable Django events and calendaring.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
