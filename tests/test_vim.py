#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import unittest
import os
import subprocess
import vimrunner


class TestVim(unittest.TestCase):
    def setUp(self):
        self._lang = os.getenv('LANG', 'C')
        os.environ['LANG'] = 'C'
        if not hasattr(subprocess, 'check_output'):
            subprocess.check_output = self.check_output
        self.server = vimrunner.Server(extra_args=['-N', '-i', 'NONE'])
        self.client = self.server.start()
        self.client.add_plugin(os.getcwd(), 'plugin/betterga.vim')
        self.client.write_buffer('1', 'a')

    def tearDown(self):
        self.server.quit()
        if subprocess.check_output == self.check_output:
            del subprocess.check_output

    def testVariableGLoadedBetterGA(self):
        self.assertEquals(self.client.echo('exists("g:loaded_betterga")'), '1')
        self.assertEquals(self.client.echo('g:loaded_betterga'), '1')

    def testVariableGBetterGATemplate(self):
        self.assertEquals(self.client.echo('exists("g:betterga_template")'), '1')
        self.assertEquals(self.client.echo('g:betterga_template'),
            '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}')

    def testVariableBBetterGATemplate(self):
        self.client.command('let b:betterga_template = "{ci.char}"')
        self.assertEquals(self.client.echo('exists("b:betterga_template")'), '1')
        self.assertEquals(self.client.echo('b:betterga_template'), '{ci.char}')
        self.assertEquals(self.client.echo('betterga#ascii()'), 'a\n0')

    def testFunctionDescribe(self):
        self.assertEquals(self.client.echo('betterga#describe("a")'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n0')

    def testFunctionAscii(self):
        self.assertEquals(self.client.echo('betterga#ascii()'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n0')

    def testCommandBetterAscii(self):
        self.assertEquals(self.client.echo('exists(":BetterAscii")'), '2')
        self.client.command('redir => g:result | BetterAscii | redir END')
        self.assertEquals(self.client.echo('g:result'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141')

    @staticmethod
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get('args')
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output
