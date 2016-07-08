#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2app

setup(
    app=['main.py'],
    data_files=[
        ('', ['project-p-tray-16-closed.png', 'project-p-tray-16-open.png']),
    ],
)
