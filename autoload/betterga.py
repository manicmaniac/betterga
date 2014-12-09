#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import unicodedata


if sys.version_info.major == 3:
    def unicode(s, encoding):
        return s


class CharInfo(object):
    def __init__(self, char):
        char = unicode(char, 'utf-8')
        assert len(char) == 1
        self._char = char
        self._ord = ord(self._char)

    def description(self, template):
        '''
        template example:
            '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}'
        '''
        return unicode(template, 'utf-8').format(ci=self)

    @property
    def char(self):
        '''
        >>> CharInfo('a').char
        u'a'
        '''
        return self._char

    @property
    def category(self):
        '''
        >>> CharInfo('a').category
        'Ll'
        '''
        return unicodedata.category(self.char)

    @property
    def name(self):
        '''
        >>> CharInfo('a').name
        'LATIN SMALL LETTER A'
        '''
        return unicodedata.name(self.char)

    @property
    def ord(self):
        '''
        >>> CharInfo('a').ord
        97
        '''
        return self._ord

    @property
    def hex(self):
        '''
        >>> CharInfo('a').hex
        '0x61'
        '''
        return hex(self.ord)

    @property
    def oct(self):
        '''
        >>> CharInfo('a').oct
        '0141'
        '''
        return oct(self.ord)

    @property
    def nfc(self):
        '''
        >>> CharInfo('a').nfc
        u'a'
        '''
        return unicodedata.normalize('NFC', self.char)

    @property
    def nfd(self):
        '''
        >>> CharInfo('a').nfc
        u'a'
        '''
        return unicodedata.normalize('NFD', self.char)


if __name__ == '__main__':
    try:
        # try to run as vim plugin
        import vim

        def betterga(char):
            if int(vim.eval('exists("b:betterga_template")')):
                template = vim.eval('b:betterga_template')
            else:
                template = vim.eval('g:betterga_template')
            encoding = vim.eval('&encoding')
            try:
                print(CharInfo(char).description(template).encode(encoding))
            except:
                vim.command('ascii')

    except ImportError:
        # run as script
        if len(sys.argv) == 2:
            (_, char) = sys.argv
            template = '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}'
        elif len(sys.argv) == 3:
            (_, char, template) = sys.argv
        else:
            print('Usage: python betterga.py char [template]')
            sys.exit(1)

        print(CharInfo(char).description(template).encode('utf-8'))

