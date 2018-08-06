# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tango-happenings',
    version='0.15.0',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    url='https://github.com/tBaxter/django-happenings',
    license='MIT',
    description='Reusable Django events and calendaring.',
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
