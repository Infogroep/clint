# -*- coding: utf-8 -*-

"""
clint.colored
~~~~~~~~~~~~~

This module provides a simple and elegant wrapper for colorama.

"""


from __future__ import absolute_import

import re
import sys

PY3 = sys.version_info[0] >= 3

from ..packages import colorama

__all__ = (
    'red', 'green', 'yellow', 'blue',
    'black', 'magenta', 'cyan', 'white',
    'bright', 'dark',
    'clean', 'disable'
)

COLORS = __all__[:-2]

if 'get_ipython' in dir():
    """
       when ipython is fired lot of variables like _oh, etc are used.
       There are so many ways to find current python interpreter is ipython.
       get_ipython is easiest is most appealing for readers to understand.
    """
    DISABLE_COLOR = True
else:
    DISABLE_COLOR = False



class ColoredString(object):
    """Enhanced string for __len__ operations on Colored output."""
    def __init__(self, color, s, setter = None, resetter = None):
        super(ColoredString, self).__init__()
        self.s = s
        self.color = color
        self.setter = setter if setter else getattr(colorama.Fore, self.color)
        self.resetter = resetter if resetter else colorama.Fore.RESET

    def __getattr__(self, att): 
             def func_help(*args, **kwargs):
                 result = getattr(self.s, att)(*args, **kwargs)
                 if isinstance(result, basestring):
                     return self._new(result)
                 elif isinstance(result, list):
                     return [self._new(x) for x in result]
                 else:
                     return result
             return func_help
       
    @property
    def color_str(self):
        if sys.stdout.isatty() and not DISABLE_COLOR:
            return '%s%s%s' % (self.setter, self.s, self.resetter)
        else:
            return self.s


    def __len__(self):
        return len(self.s)

    def __repr__(self):
        return "<%s-string: '%s'>" % (self.color, self.s)

    def __unicode__(self):
        value = self.color_str
        if isinstance(value, bytes):
            return value.decode('utf8')
        return value

    if PY3:
        __str__ = __unicode__
    else:
        def __str__(self):
            return unicode(self).encode('utf8')

    def __iter__(self):
        return iter(self.color_str)

    def __add__(self, other):
        return str(self.color_str) + str(other)

    def __radd__(self, other):
        return str(other) + str(self.color_str)

    def __mul__(self, other):
        return (self.color_str * other)

    def _new(self, s):
        return ColoredString(self.color, s, self.setter, self.resetter)


def clean(s):
    strip = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")
    txt = strip.sub('', str(s))

    strip = re.compile(r'\[\d+m')
    txt = strip.sub('', txt)

    return txt


def black(string):
    return ColoredString('BLACK', string)

def red(string):
    return ColoredString('RED', string)

def green(string):
    return ColoredString('GREEN', string)

def yellow(string):
    return ColoredString('YELLOW', string)

def blue(string):
    return ColoredString('BLUE', string)

def magenta(string):
    return ColoredString('MAGENTA', string)

def cyan(string):
    return ColoredString('CYAN', string)

def white(string):
    return ColoredString('WHITE', string)

def bright(string):
    return ColoredString('BRIGHT', string, colorama.Style.BRIGHT, colorama.Style.RESET_ALL)

def dark(string):
    return ColoredString('DARK', string, colorama.Style.DARK, colorama.Style.RESET_ALL)

def disable():
    """Disables colors."""
    global DISABLE_COLOR

    DISABLE_COLOR = True
