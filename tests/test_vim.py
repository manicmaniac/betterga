#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import unittest
import os
import headlessvim


class TestVim(unittest.TestCase):
    def setUp(self):
        env = dict(os.environ, LANG='C')
        self.vim = headlessvim.open(env=env)
        self.vim.install_plugin(os.getcwd(), 'plugin/betterga.vim')
        self.vim.send_keys('ia\033')

    def tearDown(self):
        self.vim.close()

    def testVariableGLoadedBetterGA(self):
        self.assertEqual(self.vim.echo('exists("g:loaded_betterga")'), '1')
        self.assertEqual(self.vim.echo('g:loaded_betterga'), '1')

    def testVariableGBetterGATemplate(self):
        self.assertEqual(self.vim.echo('exists("g:betterga_template")'), '1')
        self.assertEqual(self.vim.echo('g:betterga_template'),
            '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}')

    def testVariableBBetterGATemplate(self):
        self.vim.command('let b:betterga_template = "{ci.char}"')
        self.assertEqual(self.vim.echo('exists("b:betterga_template")'), '1')
        self.assertEqual(self.vim.echo('b:betterga_template'), '{ci.char}')
        self.assertEqual(self.vim.echo('betterga#ascii()'), 'a\n0')

    def testFunctionDescribe(self):
        self.assertEqual(self.vim.echo('betterga#describe("a")'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n0')

    def testFunctionAscii(self):
        self.assertEqual(self.vim.echo('betterga#ascii()'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n0')

    def testCommandBetterAscii(self):
        self.assertEqual(self.vim.echo('exists(":BetterAscii")'), '2')
        self.vim.command('redir => g:result | BetterAscii | redir END')
        self.assertEqual(self.vim.echo('g:result'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141')
