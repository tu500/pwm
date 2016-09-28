import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pwm",
    version = "0.1",
    author = "Philip Matura",
    author_email = "philip.m@tura-home.de",
    description = ("A rudimentary password manager"),
    packages=['pwm'],
    long_description=read('Readme.md'),
    entry_points='''
        [console_scripts]
        pwm=pwm.__main__:main
    ''',
)
