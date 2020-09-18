#!/usr/bin/env python3

import os
import sys
import shlex

num = str(sys.argv[1])
para = str(sys.argv[2])


def shellexec(cmd):
    return shlex.os.system(cmd)

shellexec('echo ' + num + '=' + para + ' > /dev/servoblaster')

