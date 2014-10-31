Tango Happenings
=================

[![Build Status](https://travis-ci.org/tBaxter/tango-happenings.svg?branch=master)](https://travis-ci.org/tBaxter/tango-happenings)

A powerful Django calendar/events app. It works as part of Tango, or as a standalone app.

Supports multi-day events, schedules, photos, updates, recaps and a bunch of other stuff.

Includes a copy of jquery.hcal for easy calendar creation.

Tango Happenings is tested for usage on both Python2 and Python3 installations.


## Installation:

    pip install tango-happenings

or

    pip install git+https://github.com/tBaxter/tango-happenings.git


## Usage:

Add 'happenings' and 'tango_shared' to your installed apps, then run syncdb or migrate.


## Requirements

* Installs vobject for ical/vcal integration
* Tango Shared Core
