#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh


def filetype(filepath):
    if isinstance(filepath, str):
        if filepath.startswith('~/'):
            filepath = filepath.replace('~/', sh.HOME, 1)
        return sh.file(filepath, '-b', '--mime')
    else:
        raise TypeError('argument type must be "str"')


def is_bin(filepath):
    '''
    binary file detect
    '''

    mime = filetype(filepath)
    return mime.partition(';')[0].endswith('x-executable')
