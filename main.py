#!/usr/bin/env python3

import util

print('\x1bc')  # Clear screen.

file = 'Dockerfile'

with open(file) as f:
    line = f.readline()
    n_line = 1
    instruction = ''
    while line:
        if not util.isSplittedLine(line):
            instruction = util.getInstruction(file, n_line)

        if instruction == 'COPY':
            if util.checkAlreadyCopyDestinations(line):
                print('ERROR: COPY destination already in another line.')
        print('{:03d} {:d} {:10s} | {}'.format(
            n_line,
            util.isSplittedLine(line),
            instruction,
            line), end='')
        line = f.readline()
        n_line += 1
    print(util.instCopyList)
