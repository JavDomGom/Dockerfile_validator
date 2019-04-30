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

        print('{:03d} {:d} {:10s} | {}'.format(
            n_line,
            util.isSplittedLine(line),
            instruction,
            line), end='')

        if instruction == 'COPY':
            if util.checkAlreadyCopyDestinations(line):
                print('ERROR: COPY destination already in another line.')

        if instruction == 'RUN':
            if 'apt-get install' in line:
                if util.checkRunAptGetInstall(line):
                    print('ERROR: flags "-y --no-install-recommends" not found.')

        line = f.readline()
        n_line += 1
