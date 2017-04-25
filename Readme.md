Password Manager Python Script
==============================

A rudimentary password manager. Uses a human readable "database" file format.

Features
--------

* Generate new passwords automatically
* Copy passwords to clipboard
* Interface using `dmenu`

Requirements
------------

You probably want to install the following software:

* `apg` for generating passwords
* `dmenu` for a graphical interface
* `xsel` for copying passwords to the X clipboard

How to use
----------

My standard usage:

* `pwm.py add --copy-to-clipboard --open-dmenu` to add/generate a new password
* `pwm.py show --copy-to-clipboard --quiet --augment-info --open-dmenu` to
  choose a password from the database
