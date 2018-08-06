# Tango-Happenings Change log

## 0.15.0
* Django 2.0 & Python 3.x compatible
* Fixed templates for tests
* Fixed URLs not calling views correctly
* Loosened comments dependency
* Removed permalink references

## 0.14.1, 0.14.2
Removed deprecated assignment_tags

## 0.14.0
* Updated for Django 2.0 compatibility

## 0.13.1
* Better handling of missing video module

## 0.13.0
* Improved testing and switched from vobject to python-card-me

## 0.12.4
* Attempting to import in tags to avoid loading problem.

## 0.12.3
* Reverted 12.2

## 0.12.2
* Updated template tags for 1.9

## 0.12.1
* Fix for contentType model name

## 0.12.0
* Updates for Django 1.8+ compatibility and minor cleanup

## 0.11.0
* Removed remainders of giveaways.

## 0.10.0
* Removed remainders of playlists.

## 0.9.0
* Safer static asset handling

## 0.8.7
* Sorting out EventRecapForm fields for 1.8

## 0.8.6
* Reverted to vobject.

## 0.8.5
* Cleanup on form meta.

## 0.8.4
* Attempting to force vobject version from pip.

## 0.8.3
* Incremented vobject version to force local usage.

## 0.8.2
* Cleaned up some fieldset issues

## 0.8.1
* Attempting to resolve a fields issue

## 0.8.0
* Clearer admin fieldsets and improved how-to

## 0.7.6
* Removed vobject test temporarily

## 0.7.5
* Updated to use xmltramp2

## 0.7.4
* Passing tests for python 3.4 (using vobject fork)

## 0.7.3
* Work on tests and travis integration

## 0.7.2
* Fixed problems in setup.py that were keeping dependencies from being installed.

## 0.7.1
* Using fork of vobject for proper installation

## 0.7.0
* Corrected attendee photo upload problems

## 0.6.0
* Updates for Django 1.7
* Removed admin media now defined in tango-admin

## 0.5.9
Closing stray div tag on event detail

## 0.5.8
Missed parenthesis

## 0.5.7
cleaner get_image

## 0.5.6
* get_image should not be a cached property

## 0.5.5
* Added get_image method to Event model

## 0.5.4
* Upsized sidebar images

## 0.5.3
* Fixed missing images in sidebars

## 0.5.2
* Found a stray template tag breaking update list

## 0.5.1
* Update manifest to include how-to

## 0.5.0
* Added how-to and improved admin.

## 0.4.5
* And include sortable, too.

## 0.4.4
* Corrected path to drag-and-drop image reordering js.

## 0.4.3
* Sidebar recovery

## 0.4.2
* More template revisions and updates

## 0.4.1
* Revised update slides template.

## 0.4
* Fairly major cleanup and refactor, particularly templates.

## 0.3.1
* Cleaned up some formatting
* Hid "add event" from unauthenticated users
* Fixed add event validation problem

## 0.3
Improved Event memories, updates, and photo gallery creation
