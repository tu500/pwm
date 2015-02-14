Password Manager Python Script
==============================

A rudimentary password manager. Uses a human readable "database" file format.

Features
--------

* Generate new passwords automatically
* Copy passwords to clipboard
* Interface using `dmenu`

How to use
----------

My standard usage:

* `pwm.py add --copy-to-clipboard --open-dmenu` to add/generate a new password
* `pwm.py show --copy-to-clipboard --quiet --open-dmenu` to choose a password
  from the database
