#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import unittest
import os
import subprocess
import vimrunner


class TestVim(unittest.TestCase):
    def setUp(self):
        if not hasattr(subprocess, 'check_output'):
            subprocess.check_output = self.check_output
        self.server = vimrunner.Server(extra_args=['-N', '-i', 'NONE'])
        self.client = self.server.start()
        self.client.add_plugin(os.getcwd(), 'betterga.vim')
        self.client.write_buffer("1", 'a')

    def tearDown(self):
        self.server.quit()
        if subprocess.check_output == self.check_output:
            del subprocess.check_output

    def testFunctionAscii(self):
        self.assertEquals(self.client.echo('betterga#ascii()'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n0')

    @staticmethod
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output

