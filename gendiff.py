#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sh


def get_parser():
    parser = argparse.ArgumentParser(description='compare files')
    parser.add_argument('old_file', metavar='old_file', type=str, nargs=1)
    parser.add_argument('new_file', metavar='new_file', type=str, nargs=1)
    return parser


def get_filetype(filepath):
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

    mime = get_filetype(filepath)
    return mime.partition(';')[0].endswith('x-executable')
