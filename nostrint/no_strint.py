#!usr/bin/python2
# -*- encoding:utf-8 -*-

"""

python source code obfuscator. only obscures strings and integers

"""

# <-- modules -->
from utils import utils as _utils
from obfuscator import obfuscator as _obf
from random import choice as _choice
import command_line as _command_line
from redat import *
from template import *
import sys as _sys

# <-- settings -->
reload(_sys)
_sys.setdefaultencoding('utf-8')
_sys.setrecursionlimit(999999999)

# <-- encoding -->
def encode(string_):
    """Change String to Integers"""
    return (lambda f, s: f(list( ord(c) for c in str(string_) ) , \
            s))(lambda f, s: sum(f[i] * 256 ** i for i in \
            range(len(f))), str(string_))

class strint(object):
    def __init__(self):
        self.parser = _command_line.CLI()
        self.arg = self.parser.parse_args()
        self._utils = _utils()
        self.obfuscator = _obf(self.arg, self._utils, self.en_words)
        self.set_options()
        self.begin()

    def check_syntax(self):
        # lazy script to checking syntax
        compile(open(self.arg.infile).read(), '<string>', 'exec')

    def begin(self):
        if self.arg.indent:
            if self.arg.indent < 1:
                self.parser('indentation < 1')
        if self.arg.txt or self.arg.infile:
            if self.arg.only_strint:
                if self.arg.infile:
                    self.check_syntax()  # damnit
                    _fin = self.obfuscator.rebuild()
                    if self.arg.debug or self.arg._eval or self.arg.verbose:
                        self._utils.sep('result')
                    print(_fin)
                    if self.arg.outfile:
                        self._utils.savefile(_fin, self.arg.outfile)
                else:
                    self.parser.error('argument --infile is required')
            else:
                _text = self.re_text()
                if self.arg.verbose or self.arg.debug or self.arg._eval:
                    self._utils.sep('original strint')
                    print(_text)
                _text = _text.decode('string_escape')
                if not _text.isdigit():
                    if self.arg.encode:
                        _fin = self.obfuscator.encode_base(_text)
                    else:
                        _fin = self.obfuscator.zero_base(_text)
                    # <-- next -->
                    if self.arg.stdout:
                        _fin = _choice(STDOUT_BASE).format(
                            self.obfuscator.convert(1),
                            self.obfuscator.convert(2),
                            self.obfuscator.convert(5),
                            self.obfuscator.convert(8),
                            _fin)
                    elif self.arg._exec:
                        _fin = _choice(EXEC_BASE).format(
                            self.obfuscator.zero_base('<string>'),
                            self.obfuscator.zero_base('exec'),
                            self.obfuscator.convert(1),
                            self.obfuscator.convert(95),
                            self.obfuscator.zero_base(_text),
                            self.obfuscator.convert(0))
                # <-- NOT -->
                else:
                    _fin = self.obfuscator.convert(int(_text))
                if self.arg.debug or self.arg._eval or self.arg.verbose:
                    self._utils.sep('result')
                if not self.arg.with_space:
                    _fin = self._utils.fixing(_fin)
                print(_fin)
                if self.arg._eval:
                    self._utils.sep('eval')
                    print(eval(_fin))
                if self.arg.outfile:
                    self._utils.savefile(_fin, self.arg.outfile)
        else:
            print (BANNER)
            self.parser.print_usage()

    def set_options(self):
        if self.arg.obf:
            self.arg.only_strint = True
            self.arg.ignore_comments = True
            self.arg.remove_blanks = True
            self.arg.rand_if = True
            self.arg.indent = 1
        if self.arg._exec:
            self.arg.encode = False

    def re_text(self):
        _txt = ' '.join(self.arg.txt)
        if self.arg.infile:
            _txt = open(self.arg.infile).read()
        return _txt

    def en_words(self, x):
        return ' , '.join(map(self.obfuscator.convert, map(ord, str(x))))
