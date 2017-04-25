import os
import subprocess

def copy2clipboard(string):
    """
    Use `xsel` to copy something to the X clipboard.
    """
    subprocess.check_output(['xsel', '-bi'], input=string.encode('utf8'))

def choose_entry(entries, prompt=None):
    """
    Use `dmenu` to choose an entry from a list. Can also be used as a graphical
    prompt. The `prompt` parameter controls the `dmenu`-prompt.
    """
    l = list(entries)
    l.sort()
    s = '\n'.join(l)
    if prompt is None:
        result = subprocess.check_output(['dmenu'], input=s.encode('utf8')).decode('utf8')
    else:
        result = subprocess.check_output(['dmenu', '-p', prompt], input=s.encode('utf8')).decode('utf8')
    return result[:-1] # remove newline

def generate_password(length=50):
    """
    Use `apg` to generate a new password.
    """
    result = subprocess.check_output(['apg', '-n', '1', '-m', str(length)]).decode('utf8')
    return result[:-1] # remove newline

def select_default_pwfile_path():
    """
    Return the default path for the pwfile, considering `$XDG_DATA_HOME/pws`,
    `$XDG_CONFIG_HOME/pws`, `~/.pws`.
    """
    if 'XDG_DATA_HOME' in os.environ:
        return os.path.join(os.environ['XDG_DATA_HOME'], 'pws')
    if 'XDG_CONFIG_HOME' in os.environ:
        return os.path.join(os.environ['XDG_CONFIG_HOME'], 'pws')
    return '~/.pws'
