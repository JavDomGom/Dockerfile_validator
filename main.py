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

        print('{:03d} {:d} {:10s} | {}'.format(
            n_line,
            semaphore,
            instruction,
            line), end='')

        if instruction == 'COPY':
            util.checkAlreadyCopyDestinations(line)

        if instruction == 'RUN':
            if semaphore:
                util.isOnlyOnePacketInLine(line)

                if util.isBackSlashEOL(line):
                    if util.isAndEOL(line):
                        semaphore = False
                elif len(line.split()) == 1:
                    semaphore = False

            if 'apt-get ' in line:
                option = line.split('apt-get ')[1].split()[0]
                if option == 'install':
                    semaphore = True
                util.findInRunAptGet(line, option)

            if 'pip3 install' in line:
                

        line = f.readline()
        n_line += 1