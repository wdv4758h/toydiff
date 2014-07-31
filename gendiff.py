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


def check_command(cmds=()):
    exist = {}
    for i in cmds:
        try:
            eval('sh.{}'.format(i))
            exist[i] = True
        except sh.CommandNotFound:
            exist[i] = False
    return exist


def check_shell():
    shells = ('bash', 'zsh')
    return check_command(shells)


def diff(old, new):
    # diff will return 1
    return sh.diff(old, new, _iter=True, _ok_code=[0, 1])


def xxd_diff(old, new):
    '''
    just for fun
    '''

    # xxd -p for pure hexdump
    # -p must pass in before file name

    shell = check_shell()

    # support : bash, zsh
    # not support : dash
    cmd = 'diff <(xxd -p {}) <(xxd -p {})'.format(old, new)

    if shell['bash']:
        return sh.bash('-c', cmd, _ok_code=[0, 1])
    elif shell['zsh']:
        return sh.zsh('-c', cmd, _ok_code=[0, 1])
    else:
        tmp_old = '/var/tmp/old_hex'
        tmp_new = '/var/tmp/new_hex'
        sh.xxd('-p', old, _out=tmp_old)
        sh.xxd('-p', new, _out=tmp_new)
        patch = sh.diff(old, new, _iter=True, _ok_code=[0, 1])
        sh.rm('-f', tmp_old)
        sh.rm('-f', tmp_new)
        return patch


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    old_file = args['old_file'][0]
    new_file = args['new_file'][0]

    binary = is_bin(old_file)

    if binary:
        patch = xxd_diff(old_file, new_file)
    else:
        patch = diff(old_file, new_file)

    print(patch)

if __name__ == '__main__':
    main()
