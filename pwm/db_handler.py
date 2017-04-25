import codecs
import re

def parse_dbfile(filename):
    """
    Parse a pwm db file. Return a dictionary of all entries.

    The keys are entry names, the values are tuples of the stored pw and info
    field.
    """

    with codecs.open(filename, 'rb', encoding='utf8') as f:
        lines = f.readlines()

    return parse_db(lines, filename=filename)

def parse_db(lines, filename='-'):
    """
    Parse a db from memory. The parameter `lines` should be an iterable of
    strings representing lines of a db file.

    The `filename` parameter is used in possible parsing failure messages.
    """

    entries = {}

    it = iter(enumerate(lines, 1))

    try:
        while True:
            lineno, l = next(it)
            l = l.rstrip()

            if l.startswith('#') or not l:
                continue

            match = re.match(r'^(?P<name>.*):(?: (?P<info>.*))? +(?P<pw>[^ ]+)$', l)

            if match:
                entries[match.group('name')] = match.group('pw', 'info')
                continue

            if not l.endswith(':'):
                raise Exception('Parsing Failed: "{}" line {}'.format(filename, lineno))

            name = l[:-1]
            lineno, l = next(it)
            l = l.rstrip()
            match = re.match(r'^  (?:(?P<info>.*) +)?(?P<pw>[^ ]+)$', l)

            if match:
                entries[name] = match.group('pw', 'info')
                continue
            else:
                raise Exception('Parsing Failed: "{}" line {}'.format(filename, lineno))

    except StopIteration:
        pass

    return entries

def add_entry(filename, name, pw, info=None, check_if_exists=True):
    """
    Append a single entry to a db file. Optionally first check whether an entry
    with that name already exists. An exception is thrown in this case.

    Performs no error checking.
    """

    if check_if_exists:
        try:
            entries = parse_dbfile(filename)
            if name in entries:
                raise Exception('Entry already exists: ' + repr(name))
        except FileNotFoundError:
            pass

    if info is None:
        #s = '{name}: {pw}\n'.format(name=name, pw=pw)
        s = '{name}:\n  {pw}\n'.format(name=name, pw=pw)
    else:
        s = '{name}:\n  {info} {pw}\n'.format(name=name, pw=pw, info=info)

    with codecs.open(filename, 'ab', encoding='utf8') as f:
        f.write(s)

def remove_entry(filename, name_to_remove, ignore_non_existing=False, remove_multiple=False):
    """
    Remove a single entry from a db file. Throws an exception if it does not
    exist or does exist multiple times. This behaviour can be overriden with
    the `ignore_non_existing` and `remove_multiple` arguments.
    """

    with codecs.open(filename, 'rb', encoding='utf8') as f:
        lines = f.readlines()

    updated_lines = []
    entry_count = 0

    it = iter(enumerate(lines, 1))

    try:
        while True:
            l = next(it).rstrip()

            if l.startswith('#') or not l:
                updated_lines.append(l)
                continue

            match = re.match(r'^(?P<name>.*):(?: (?P<info>.*))? +(?P<pw>[^ ]+)$', l)

            if match:
                if match.group('name') == name_to_remove:
                    entry_count +=1
                    # don't add this line
                    continue
                else:
                    updated_lines.append(l)
                    continue

            if not l.endswith(':'):
                raise Exception('Parsing Failed: "{}" line {}'.format(filename, lineno))

            first_line = l
            name = l[:-1]

            second_line = next(it).rstrip()
            match = re.match(r'^  (?:(?P<info>.*) +)?(?P<pw>[^ ]+)$', second_line)

            if match:
                if name == name_to_remove:
                    entry_count +=1
                    # don't add these two lines
                    continue
                else:
                    updated_lines.append(first_line)
                    updated_lines.append(second_line)
                    continue

            else:
                raise Exception('Parsing Failed: "{}" line {}'.format(filename, lineno))

    except StopIteration:
        pass

    if entry_count == 0:
        if not ignore_non_existing:
            raise Exception('Item does not exist.')
        else:
            return

    if entry_count > 1 and not remove_multiple:
        raise Exception('Item found multiple times.')

    with codecs.open(filename, 'wb', encoding='utf8') as f:
        f.write('\n'.join(updated_lines) + '\n')
