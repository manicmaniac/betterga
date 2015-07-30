#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import unittest
import subprocess
import sys
import os


class TestBetterGA(unittest.TestCase):
    script_file_path = 'autoload/betterga.py'

    def testUsage(self):
        ret, out, err = self.betterga()
        self.assertEquals(ret, 1)
        self.assertEquals(out.decode(),
            'Usage: python betterga.py char [template]\n')

    def testDescription(self):
        ret, out, err = self.betterga('a')
        self.assertEquals(ret, 0)
        self.assertEquals(out.decode(),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n')

    def testDescriptionUnicodeCharacter(self):
        if os.name == 'nt':
            encoding = 'cp932'
        else:
            encoding = sys.getfilesystemencoding()
        ret, out, err = self.betterga('\u86c7', PYTHONIOENCODING=encoding)
        self.assertEquals(ret, 0)
        self.assertEquals(out.decode(encoding),
            '<\u86c7> [CJK UNIFIED IDEOGRAPH-86C7] 34503, Hex 0x86c7, Octal 0103307\n')

    def testDescriptionWithTemplate(self):
        ret, out, err = self.betterga('a', '{ci.char}')
        self.assertEquals(ret, 0)
        self.assertEquals(out.decode(), 'a\n')

    def testExposeOnlyOneNameToGlobalNamespace(self):
        import autoload.betterga as betterga
        import tests.fixtures.empty_module as empty_module
        self.assertEqual(len(dir(betterga)), len(dir(empty_module)) + 1)
        del betterga
        del empty_module

    def betterga(self, *args, **env):
        args = [sys.executable, self.script_file_path] + list(args)
        process = subprocess.Popen(args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ, **env))
        out, err = process.communicate()
        return process.returncode, out, err
