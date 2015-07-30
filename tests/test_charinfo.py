#!/usr/bin/env python
# -*- coding:utf-8 -*-

import doctest
import autoload.betterga


def load_tests(loader, tests, ignore):
    return doctest.DocTestSuite(autoload.betterga)
