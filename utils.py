#!/usr/bin/env python
# -*- coding: utf-8 -*-
# utils.py - 2021/10/9
#
import os
import shutil

from settings import BASEDIR


def makedir(directory, clean=False):
    """
    make a specific directory under the project,
    delete existing directory and all its contents if clean is False.
    """
    if os.path.exists(directory):
        if clean:
            shutil.rmtree(os.path.join(BASEDIR, directory))
    else:
        os.mkdir(os.path.join(BASEDIR, directory))
