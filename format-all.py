#!/usr/bin/env python
from __future__ import print_function

import fnmatch
import os
import subprocess
import sys
import glob

path = os.path.dirname(os.path.realpath(__file__))

masks = ['*.hpp', '*.h', '*.cpp', '*.c', '*.cxx']
ignore = ['build/*', 'build-*', 'cmake-*', '.*', 'include/kfr/io/dr']

filenames = []
for root, dirnames, files in os.walk(path, path):
    ignore_dir = any(
        fnmatch.fnmatch(os.path.relpath(root, path), mask) for mask in ignore
    )
    if not ignore_dir:
        for mask in masks:
            filenames.extend(
                os.path.join(root, filename)
                for filename in fnmatch.filter(files, mask)
            )
for filename in filenames:
    print( filename, '...' )
    subprocess.call(['clang-format', '-i', filename])
    # Fix clang-format bug: https://llvm.org/bugs/show_bug.cgi?id=26125
    for tmp_file in glob.glob(f'{filename}*.tmp'):
        os.remove(tmp_file)
