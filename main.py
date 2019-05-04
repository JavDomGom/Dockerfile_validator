#!/usr/bin/env python3

import util

print('\x1bc')  # Clear screen.

file = 'Dockerfile'

with open(file) as f:
    line = f.readline()
    nLine = 1
    instruction = ''
    labelInstruction = False
    semaphorePack = False
    semaphoreRemove = False
    nRemoveLine = 0

    while line:
        if not util.isSplittedLine(line):
            instruction = util.getInstruction(file, nLine)

        if instruction == '':
            util.isOutOfInstruction(line)
            semaphoreRemove = False

        print('{:03d} {:10s} | {}'.format(
            nLine,
            instruction,
            line), end='')

        if instruction == 'COPY':
            util.checkAlreadyCopyDestinations(line)

        if instruction == 'RUN':
            if semaphorePack:
                util.isOnlyOnePacketInLine(line)

                if util.isBackSlashEOL(line):
                    if util.isAndEOL(line):
                        semaphorePack = False
                elif len(line.split()) == 1:
                    semaphorePack = False
                    instruction = ''

            if 'apt-get ' in line:
                option = line.split('apt-get ')[1].split()[0]
                if option == 'install':
                    semaphorePack = True
                util.findInRunAptGet(line, option)

            if 'pip3 install' in line:
                util.findInPipInstall(line)

            if 'rm -' in line:
                if semaphoreRemove:
                    util.printAlreadyRemoveInBlock(nRemoveLine)

                nRemoveLine = nLine
                semaphoreRemove = True

        if instruction == 'LABEL':
            labelInstruction = True
            util.findInLabel(line)

        if not labelInstruction:
            pass

        line = f.readline()
        nLine += 1
