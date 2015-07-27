#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import subprocess
import sys

class TestBetterGA(unittest.TestCase):
    def testUsage(self):
        ret, out, err = self.betterga()
        self.assertEqual(ret, 1)
        self.assertEqual(out.decode(), 'Usage: python betterga.py char [template]\n')

    def testDescription(self):
        ret, out, err = self.betterga('a')
        self.assertEqual(ret, 0)
        self.assertEqual(out.decode(), '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n')

    def testDescriptionWithTemplate(self):
        ret, out, err = self.betterga('a', '{ci.char}')
        self.assertEqual(ret, 0)
        self.assertEqual(out.decode(), 'a\n')

    def betterga(self, *args):
        args = list(args)
        args.insert(0, sys.executable)
        args.insert(1, 'autoload/betterga.py')
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = process.communicate()
        return process.returncode, out, err

