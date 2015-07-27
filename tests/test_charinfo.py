#!/usr/bin/env python
# -*- coding:utf-8 -*-

import doctest
import unittest
import autoload.betterga

def load_tests(loader, tests, ignore):
    suite = unittest.TestSuite(doctest.DocTestSuite(autoload.betterga))
    return suite

