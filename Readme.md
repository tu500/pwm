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

A Word about Security
---------------------

Pwm stores passwords **unencrypted** in a plain text database file. It does
**not** obfuscate or encrypt them using a master password.

The reasoning behind this is as follows: In general the applied threat models
boil down to:

1. Someone gains access to your running system.
2. Someone gains access to your non-running system (ie. disk drive).

In my (arguably simplified) reasoning, the remedies to these are:

1. You're fucked anyway.
2. Use full disk encryption.

If you want further protection considering the first case you should look into
something like the `pass` program (see [below](#similar-software)).

*Note:* For you, other threat models may apply. Use this program at your own
risk.

Similar Software
-----------------

* [pass](https://www.passwordstore.org/)
