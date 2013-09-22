#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess


def fortune_teller():
    p = subprocess.Popen(['fortune', '-s'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, errors = p.communicate()
    return output




















