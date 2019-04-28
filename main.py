#!/usr/bin/env python3

import util

print('\x1bc')  # Clear screen.

file = 'Dockerfile'

with open(file) as f:
    line = f.readline()
    n_line = 1
    var = ''
    while line:
        if not util.isSplittedLine(line):
            var = util.getInstruction(file, n_line)

        print('{:03d} {:d} {:10s} | {}'.format(
            n_line,
            util.isSplittedLine(line),
            var,
            line), end='')
        line = f.readline()
        n_line += 1
