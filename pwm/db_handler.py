import re
import codecs

def parse_dbfile(filename):
    """
    Parse a pwm db file. Return a dictionary of all entries.

    The keys are entry names, the values are tuples of the stored pw and info
    field.
    """

    with codecs.open(filename, 'rb', encoding='utf8') as f:
        lines = f.readlines()

    return parse_db(lines)

def parse_db(lines):
    """
    Parse a db from memory. The parameter `lines` should be an iterable of
    strings representing lines of a db file.
    """

    entries = {}

    it = iter(lines)

    try:
        while True:
            l = next(it).rstrip()

            if l.startswith('#') or not l:
                continue

            match = re.match(r'^(?P<name>.*):(?: (?P<info>.*))? +(?P<pw>[^ ]+)$', l)

            if match:
                entries[match.group('name')] = match.group('pw', 'info')
                continue

            if not l.endswith(':'):
                raise Exception("Parsing Failed: " + repr(l))

            name = l[:-1]
            l = next(it).rstrip()
            match = re.match(r'^  (?:(?P<info>.*) +)?(?P<pw>[^ ]+)$', l)

            if match:
                entries[name] = match.group('pw', 'info')
                continue
            else:
                raise Exception("Parsing Failed: " + repr(l))

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
                raise Exception("Entry already exists: " + repr(name))
        except FileNotFoundError:
            pass

    if info is None:
        #s = '{name}: {pw}\n'.format(name=name, pw=pw)
        s = '{name}:\n  {pw}\n'.format(name=name, pw=pw)
    else:
        s = '{name}:\n  {info} {pw}\n'.format(name=name, pw=pw, info=info)

    with codecs.open(filename, 'ab', encoding='utf8') as f:
        f.write(s)
