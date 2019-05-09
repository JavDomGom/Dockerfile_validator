#!/usr/bin/env python3

import sys
import util

util.checkArgs(sys.argv)
util.clearScreen()

# Set global variables.
dockerfile      = sys.argv[1]
nLine           = 1
instruction     = ''
userInstruction = False
semaphorePack   = False
semaphoreRemove = False
nRemoveLine     = 0
labelOptions    = {}

with open(dockerfile) as f:
    line = f.readline()
    util.printHeader()

    while line:

        # Reset to OK by default.
        status = 'OK'

        if not util.isSplittedLine(line):
            instruction = util.getInstruction(dockerfile, nLine)

        if instruction == '':
            if util.isOutOfInstruction(line):
                status = 'ERROR'
            else:
                status = ''
            semaphoreRemove = False

        if instruction == 'COPY':
            if util.checkAlreadyCopyDestinations(line):
                status = 'ERROR'

        if instruction == 'RUN':
            if semaphorePack:
                if util.isMoreThanOnePackagePerLine(line):
                    status = 'ERROR'

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

                if util.findInRunAptGet(line, option):
                    status = 'ERROR'

            if 'pip3 install' in line:
                if util.findInPipInstall(line):
                    status = 'ERROR'

            if 'rm -' in line:
                if semaphoreRemove:
                    util.printAlreadyRemoveInBlock(nRemoveLine)
                    status = 'ERROR'

                nRemoveLine = nLine
                semaphoreRemove = True

        if instruction == 'LABEL':
            labelOptions = util.getLabelOptions(line)

        if instruction == 'USER':
            userInstruction = True

        util.printCheckedLine(nLine, status, line)

        line = f.readline()
        nLine += 1

    util.findInLabelOptions(labelOptions)
    util.isUserInstruction(userInstruction)
