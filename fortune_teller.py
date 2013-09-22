#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fortune

files = ['fortune/freebsd', 'fortune/kernel']


def fortune_teller():
    i = fortune.random_int(0, len(files) - 1)
    quote = fortune.get_random_fortune(files[i])
    if quote[0:2] == "%\n":
        return quote[2:]
    return quote
