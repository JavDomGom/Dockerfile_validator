#!/usr/bin/env python3

import util

print('\x1bc')  # Clear screen.

file = 'Dockerfile'

with open(file) as f:
    line = f.readline()
    n_line = 1
    instruction = ''
    semaphore = False

    while line:
        if not util.isSplittedLine(line):
            instruction = util.getInstruction(file, n_line)

        if instruction == 'COPY':
            util.checkAlreadyCopyDestinations(line)

        print('{:03d} {:10s} | {}'.format(
            n_line,
            instruction,
            line), end='')

        if instruction == 'RUN':
            if semaphore:
                util.isOnlyOnePacketInLine(line)

            if 'apt-get ' in line:
                option = line.split('apt-get ')[1].split()[0]
                if option == 'install':
                    semaphore = True
                util.findInRunAptGet(line, option)
            if util.isAndEOL(line) and util.isBackSlashEOL(line):
                semaphore = False

        line = f.readline()
        n_line += 1
