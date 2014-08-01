#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sh


def bspatch(old, new, patch):
    if new:
        sh.bspatch(old, new, patch)
    else:
        sh.bspatch(old, old+'.new', patch)


def patch(old, new, patch):
    if new:
        sh.cp('-f', old, new)
        sh.patch(new, patch)
    else:
        sh.patch(old, patch)


def xxd_patch(old, new, patch):
    tmp_old = '/var/tmp/old_hex'
    sh.xxd('-p', old, _out=tmp_old)
    sh.tail('-n', '+2', patch, _out=patch+'.nohead')
    sh.patch(tmp_old, patch+'.nohead')

    if new:
        sh.xxd('-r', '-p', tmp_old, _out=new)
    else:
        sh.xxd('-r', '-p', tmp_old, _out=old)

    sh.rm('-f', tmp_old)
