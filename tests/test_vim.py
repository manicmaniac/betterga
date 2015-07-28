#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import unittest
import os
import subprocess


if not hasattr(subprocess, 'check_output'):
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
    subprocess.check_output = check_output
import vimrunner


class TestVim(unittest.TestCase):
    def setUp(self):
        self.server = vimrunner.Server(extra_args=['-N', '-i', 'NONE'])
        self.client = self.server.start()
        self.client.add_plugin(os.getcwd(), 'betterga.vim')
        self.client.write_buffer("1", 'a')

    def tearDown(self):
        self.server.quit()

    def testFunctionAscii(self):
        self.assertEquals(self.client.echo('betterga#ascii()'),
            '<a> [LATIN SMALL LETTER A] 97, Hex 0x61, Octal 0141\n0')

