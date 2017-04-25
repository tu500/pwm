#!/usr/bin/python3
import argparse
import os
import re
import sys

from . import db_handler
from . import helpers

def run_add_entry(args):
    pwfile = os.path.expanduser(args.pwfile)

    if args.open_dmenu:

        try:
            entry_name = helpers.choose_entry([], prompt='>>> New Password >>>')

        except FileNotFoundError:
            print('Could not find dmenu binary, is it installed and in PATH?')
            sys.exit(1)

        match = re.match(r'^(?P<name>.*): (?P<info>.*)$', entry_name)
        #if match and args.info is None:
        if match:
            entry_name = match.group('name')
            entry_info = match.group('info')
        else:
            entry_info = args.info

    else:
        entry_name = args.name
        entry_info = args.info

    if args.password is None:

        try:
            pw = helpers.generate_password(length=args.length)

        except FileNotFoundError:
            print('Could not find apg binary, is it installed and in PATH?')
            sys.exit(1)

    else:
        pw = args.password

    if args.clipboard:

        try:
            helpers.copy2clipboard(pw)

        except FileNotFoundError:
            print('Could not find xsel binary, is it installed and in PATH?')
            sys.exit(1)

    db_handler.add_entry(pwfile, entry_name, pw, entry_info)

def run_print_entry(args):
    pwfile = os.path.expanduser(args.pwfile)

    try:
        entries = db_handler.parse_dbfile(pwfile)
    except FileNotFoundError:
        print('Password database file `{}` not found. Use `pwm add` to create db file.'.format(pwfile))
        sys.exit(1)

    if args.open_dmenu:

        try:
            entry_name = helpers.choose_entry(entries.keys())

        except FileNotFoundError:
            print('Could not find dmenu binary, is it installed and in PATH?')
            sys.exit(1)

    else:
        entry_name = args.name

    if not entry_name in entries:
        raise Exception("No such entry")

    entry_pw, entry_info = entries[entry_name]

    if not args.quiet:
        if args.output is None:
            print(entry_pw)
        else:
            for i in args.output:
                if i == 'info':
                    print(entry_info)
                elif i == 'pw':
                    print(entry_pw)
                elif i == 'name':
                    print(entry_name)

    if args.clipboard:

        try:
            helpers.copy2clipboard(entry_pw)

        except FileNotFoundError:
            print('Could not find xsel binary, is it installed and in PATH?')
            sys.exit(1)

def run_list_entries(args):
    pwfile = os.path.expanduser(args.pwfile)

    try:
        entries = db_handler.parse_dbfile(pwfile)
    except FileNotFoundError:
        print('Password database file `{}` not found. Use `pwm add` to create db file.'.format(pwfile))
        sys.exit(1)

    keys = list(entries.keys())
    keys.sort()
    for i in keys:
        print(i)

def main():
    parser = argparse.ArgumentParser(
            description='Password Manager')

    parser.add_argument('--password-file', dest='pwfile', default=helpers.select_default_pwfile_path(), help='File which stores the passwords')

    subparsers = parser.add_subparsers(title='Subcommands')

    parser_add = subparsers.add_parser('add', help='Add a new password entry')
    entry_name_group = parser_add.add_mutually_exclusive_group(required=True)
    entry_name_group.add_argument('name', nargs='?', help='Name of entry to display')
    entry_name_group.add_argument('-d', '--open-dmenu', action='store_true', help='Instead of taking the entry name on the commandline, open a dmenu list to enter a name. Additionally an info can be given with the format `entry name: info`')
    parser_add.add_argument('-i', '--info', default=None, help='Additional info (user name, ...)')
    parser_add.add_argument('-p', '--password', default=None, help='Password to store. If not given, a new one is generated.')
    parser_add.add_argument('-l', '--length', default=50, type=int, metavar='N', help='Length of password to be generated')
    parser_add.add_argument('-c', '--copy-to-clipboard', dest='clipboard', action='store_true', help='Copy password to clipboard')
    parser_add.set_defaults(func=run_add_entry)

    parser_print = subparsers.add_parser('show', help='Print the password corresponding to some entry')
    entry_name_group = parser_print.add_mutually_exclusive_group(required=True)
    entry_name_group.add_argument('name', nargs='?', help='Name of entry to display')
    entry_name_group.add_argument('-d', '--open-dmenu', action='store_true', help='Instead of taking the entry name on the commandline, open a dmenu list to choose an entry')
    parser_print.add_argument('-c', '--copy-to-clipboard', dest='clipboard', action='store_true', help='Copy found password entry to clipboard')
    output_group = parser_print.add_argument_group(title='output', description='Specified fields will be printed, on separate lines, in the order given. Default is `--print-password` only.')
    output_group.add_argument('-q', '--quiet', action='store_true', help='No output. Overrides `--print-*` flags')
    output_group.add_argument('--print-name', dest='output', action='append_const', const='name', help='Print entry name')
    output_group.add_argument('--print-password', dest='output', action='append_const', const='pw', help='Print entry password')
    output_group.add_argument('--print-info', dest='output', action='append_const', const='info', help='Print entry info')
    parser_print.set_defaults(func=run_print_entry)

    parser_list = subparsers.add_parser('list', help='List all available entries')
    parser_list.set_defaults(func=run_list_entries)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()
