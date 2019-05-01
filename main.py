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

        print('{:03d} {:10s} | {}'.format(
            n_line,
            instruction,
            line), end='')

        if instruction == 'COPY':
            util.checkAlreadyCopyDestinations(line)

        if instruction == 'RUN':
            if 'apt-get ' in line:
                option = line.split('apt-get ')[1].split()[0]
                isPackage = option == 'install'

                util.findInRunAptGet(line, option)

        line = f.readline()
        n_line += 1
