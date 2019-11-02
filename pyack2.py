#!/usr/bin/env python

# pyack.py but with threads.

import os
import sys
import re

from queue import Queue
import threading

q = Queue()

def findhits():
    filepath, regex = q.get()
    any_printed = False
    with open(filepath, 'r', encoding='ISO8859') as fh:
        n = 0
        line = fh.readline()
        while line:
            n += 1
            match = regex.search(line)
            if match:
                if not any_printed:
                    print(filepath)
                    any_printed = True
                line = line.rstrip()
                print(str(n) + ': ' + line)
            line = fh.readline()
        fh.close()

thread = threading.Thread(target=findhits)
thread.start()

# Set the directory you want to start from
text_regex = sys.argv[1]
rootDir = sys.argv[2]
gitpath = rootDir + '/.git'
regex = re.compile(text_regex)


#thread.join()
swapfile_regex = re.compile('\\.swp$')
tilde_regex = re.compile('~$')
graphic_regex = re.compile('\\.(png|ico|gif)$')
garbage_regex = re.compile('\\.(pbc|gz)$')
for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        if fname == 'string_cs.t':
            continue
        if fname == 'POD2HTML.pm':
            continue
        if swapfile_regex.search(fname):
            continue
        if tilde_regex.search(fname):
            continue
        if graphic_regex.search(fname):
            continue
        if garbage_regex.search(fname):
            continue
        # Put our file in the queue, rather than calling findhits
        q.put([dirpath + '/' + fname, regex])
