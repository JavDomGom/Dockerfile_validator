#!/usr/bin/env python3

instCopyList = []


def isSplittedLine(line):
    '''Check if line starts with a space (splitted line).
    Attributes:
        :line: Dockerfile reading line.
    '''
    return line[0] == ' '


def isBackSlashEOL(line):
    return line.split()[-1] == '\\'


def isAndEOL(line):
    return line.split()[-2] == '&&'


def getInstruction(file, n_line):
    with open(file) as f:
        return f.read().split('\n')[n_line - 1].split(' ')[0]


def checkAlreadyCopyDestinations(line):
    destination = line.split()[-1]
    if destination in instCopyList:
        print('ERROR: COPY destination already in another line.')
        return True
    else:
        instCopyList.append(destination)
        return False


def isOnlyOnePacketInLine(line):
    if len(line.split()) == 1:
        maxLen = 1
    elif isAndEOL(line):
        maxLen = 3
    elif isBackSlashEOL(line):
        maxLen = 2

    if len(line.split()) > maxLen:
        print('ERROR: It\'s preferable to specify only ' +
              'one packet per line.')


def findInRunAptGet(line, option):

    if option == 'update':
        if not isAndEOL(line) or not isBackSlashEOL(line):
            print('ERROR: This line must end with "&& \\".')
            return True

    if option == 'install':
        if '-y --no-install-recommends' not in line:
            print('ERROR: "-y --no-install-recommends" not found.')
            return True

        if isAndEOL(line):
            print('ERROR: This line shouldn\'t contain "&&".')
            return True

        if not isBackSlashEOL(line):
            print('ERROR: This line must end with "\\".')
            return True

    if option == 'upgrade':
        print('ERROR: It\'s not recomendable to use "upgrade".')
        return True


def findInPipInstall(line):
    if '-Ur requirements.txt' not in line:
        print('ERROR: "-y --no-install-recommends" not found.')
        return True