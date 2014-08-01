#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sh
from toydiff import get_filetype, homedir_replace


def get_parser():
    parser = argparse.ArgumentParser(description='compare files')
    add_arg = parser.add_argument
    add_arg('old_file', metavar='old_file', type=str, nargs=1)
    add_arg('patch', metavar='patch', type=str, nargs=1)
    add_arg('output_file', metavar='new_file', type=str, nargs='?', default='')
    return parser


def get_patchtype(filepath):
    mime = get_filetype(filepath)
    mime_pre = mime.partition(';')[0]
    if mime_pre == 'text/plain':
        head = sh.head('-n1', filepath).strip()
        if head == 'xxd_diff':
            return 'xxd_diff'
        else:
            return 'patch'
    elif mime.strip().endswith('=binary'):
        return 'binary'


def bspatch(old, new, patch_file):
    if new:
        sh.bspatch(old, new, patch_file)
    else:
        sh.bspatch(old, old+'.new', patch_file)


def patch(old, new, patch_file):
    if new:
        sh.cp('-f', old, new)
        sh.patch(new, patch_file)
    else:
        sh.patch(old, patch_file)


def xxd_patch(old, new, patch_file):
    tmp_old = '/var/tmp/old_hex'
    sh.xxd('-p', old, _out=tmp_old)
    sh.tail('-n', '+2', patch_file, _out=patch_file+'.nohead')
    sh.patch(tmp_old, patch_file+'.nohead')

    if new:
        sh.xxd('-r', '-p', tmp_old, _out=new)
    else:
        sh.xxd('-r', '-p', tmp_old, _out=old)

    sh.rm('-f', tmp_old)
    sh.rm('-f', patch_file+'.nohead')


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    old_file = args['old_file'][0]
    patch_file = args['patch'][0]
    output_file = args['output_file']

    old_file = homedir_replace(old_file)
    patch_file = homedir_replace(patch_file)
    output_file = homedir_replace(output_file)

    patch_type = get_patchtype(patch_file)

    if patch_type == 'binary':
        bspatch(old_file, output_file, patch_file)
    elif patch_type == 'xxd_diff':
        xxd_patch(old_file, output_file, patch_file)
    else:
        patch(old_file, output_file, patch_file)


if __name__ == '__main__':
    main()
