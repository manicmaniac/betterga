#!/usr/bin/env python
# -*- coding:utf-8 -*-


class BetterGA(object):
    class CharInfo(object):
        import unicodedata # flake8: noqa

        def __init__(self, char):
            '''
            >>> BetterGA.CharInfo('a') # doctest: +ELLIPSIS
            <...betterga....CharInfo object at 0x...>

            >>> BetterGA.CharInfo('spam')
            Traceback (most recent call last):
            ...
            AssertionError
            '''
            try:
                char = char.decode('utf-8')
            except AttributeError:
                pass
            assert len(char) == 1
            self._char = char
            self._ord = ord(self._char)

        def description(self, template):
            '''
            >>> str(BetterGA.CharInfo('a').description(
            ...     '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}'))
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141'
            '''
            try:
                template = template.decode('utf-8')
            except AttributeError:
                pass
            return template.format(ci=self)

        @property
        def char(self):
            '''
            >>> str(BetterGA.CharInfo('a').char)
            'a'
            '''
            return self._char

        @property
        def category(self):
            '''
            >>> BetterGA.CharInfo('a').category
            'Ll'
            '''
            return self.unicodedata.category(self.char)

        @property
        def name(self):
            '''
            >>> BetterGA.CharInfo('a').name
            'LATIN SMALL LETTER A'
            '''
            return self.unicodedata.name(self.char)

        @property
        def ord(self):
            '''
            >>> BetterGA.CharInfo('a').ord
            97
            '''
            return self._ord

        @property
        def hex(self):
            '''
            >>> BetterGA.CharInfo('a').hex
            '0x61'
            '''
            return hex(self.ord)

        @property
        def oct(self):
            '''
            >>> BetterGA.CharInfo('a').oct
            '0141'
            '''
            return oct(self.ord).replace('o', '')

        @property
        def nfc(self):
            '''
            >>> str(BetterGA.CharInfo('a').nfc)
            'a'
            '''
            return self.unicodedata.normalize('NFC', self.char)

        @property
        def nfd(self):
            '''
            >>> str(BetterGA.CharInfo('a').nfd)
            'a'
            '''
            return self.unicodedata.normalize('NFD', self.char)

    @staticmethod
    def betterga(char):
        if int(vim.eval('exists("b:betterga_template")')):
            template = vim.eval('b:betterga_template')
        else:
            template = vim.eval('g:betterga_template')
        encoding = vim.eval('&encoding')
        try:
            print(BetterGA.CharInfo(char).description(template).encode(encoding))
        except:
            vim.command('ascii')


if __name__ == '__main__':
    try:
        # try to run as vim plugin
        import vim

    except ImportError:
        # run as script
        import sys
        if len(sys.argv) == 2:
            (_, char) = sys.argv
            template = '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}'
        elif len(sys.argv) == 3:
            (_, char, template) = sys.argv
        else:
            print('Usage: python betterga.py char [template]')
            sys.exit(1)

        print(BetterGA.CharInfo(char).description(template))
