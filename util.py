#!/usr/bin/env python3

import sys

# Set global variables.
instCopyList = []
labelOptions = {'version': False,
                'description': False,
                'maintainer': False}


def clearScreen():
    ''' Just clear screen. '''
    print('\x1bc')


def printHeader():
    ''' Just print left column header. '''

    print('Line  Status \u2551')
    print(('\u2550' * 13) + '\u2563')


def textGreen(string):
    ''' This method returns a string formatted with green color.

    Attributes:
        :string: Some string.
    '''

    return '\033[92m{:6s}\033[00m'.format(string)


def textRed(string):
    ''' This method returns a string formatted with red color.

    Attributes:
        :string: Some string.
    '''

    return '\033[91m{:6s}\033[00m'.format(string)


def getColoredStatus(status):
    ''' This method returns status with format.

    Attributes:
        :status: Status from line.
    '''

    if status == 'OK' or status == '':
        return textGreen(status)
    elif status == 'ERROR':
        return textRed(status)


def printError(msg):
    ''' This method prints an error message with format.

    Attributes:
        :msg: Error message.
    '''

    print((' ' * 13) + '\u2551     ' + textRed(msg))


def checkArgs(arguments):
    ''' Check that the program receives Dockerfile as argument.

    Attributes:
        :arguments: Arguments array.
    '''

    if len(arguments) <= 1 or arguments[1] != 'Dockerfile':
        printError('Missing Dockerfile as argument.')
        sys.exit()


def isSplittedLine(line):
    ''' Check if line starts with a space (splitted line).

    Attributes:
        :line: Dockerfile current line.
    '''

    return line[0] == ' '


def isOutOfInstruction(line):
    ''' Check if the line doesn\'t belong to any Docker instruction.

    Attributes:
        :line: Dockerfile current line.
    '''

    if isSplittedLine(line) and len(line.split()) > 0:
        printError('Line without parent instruction.')
        return True


def isBackSlashEOL(line):
    ''' Check if there is a backslash at the end of the line.

    Attributes:
        :line: Dockerfile current line.
    '''

    return line.split()[-1] == '\\'


def isAndEOL(line):
    ''' Check if there is a logic AND (&&) at the end of the line.

    Attributes:
        :line: Dockerfile current line.
    '''

    return line.split()[-2] == '&&'


def getInstruction(dockerfile, nLine):
    ''' This method returns the Docker instruction from the previous
        line to the current one.

    Attributes:
        :dockerfile:    Dockerfile to read.
        :nLine:         Current line number.
    '''

    with open(dockerfile) as f:
        # Get instruction from the previous line "nLine - 1".
        return f.read().split('\n')[nLine - 1].split(' ')[0]


def checkAlreadyCopyDestinations(line):
    ''' Check if there is more than one COPY instruction with the
        same destination.

    Attributes:
        :line: Dockerfile current line.
    '''

    destination = line.split()[-1]
    if destination in instCopyList:
        printError('Destination in COPY instruction found in another line.')
        return True
    else:
        instCopyList.append(destination)
        return False


def isMoreThanOnePackagePerLine(line):
    ''' Check that when the "apt-get install" program is executed,
        one package per line is specified.

    Attributes:
        :line: Dockerfile current line.
    '''

    if len(line.split()) == 1:
        maxLen = 1
    elif isAndEOL(line):
        maxLen = 3
    elif isBackSlashEOL(line):
        maxLen = 2

    if len(line.split()) > maxLen:
        printError('It\'s preferable to specify only one packet per line.')
        return True


def findInRunAptGet(line, option):
    ''' This method evaluates if you are invoking correctly some
        options that the "apt-get" program can receive.

    Attributes:
        :line:      Dockerfile current line.
        :option:    Specified option when executing the "apt-get"
                    program. For example update, upgrade, instal, etc.
    '''

    if option == 'update':
        if not isAndEOL(line) or not isBackSlashEOL(line):
            printError('This line must end with "&& \\".')
            return True

    if option == 'install':
        if '-y --no-install-recommends' not in line:
            printError('"-y --no-install-recommends" not found.')
            return True

        if isAndEOL(line):
            printError('This line shouldn\'t contain "&&".')
            return True

        if not isBackSlashEOL(line):
            printError('This line must end with "\\".')
            return True

    if option == 'upgrade':
        printError('It\'s not recomendable to use "upgrade" option.')
        return True


def findInPipInstall(line):
    ''' Check if the "pip3" program with the "install" option is executed
        with "-Ur" flag and a file where the packages to be installed are
        specified as argument.

    Attributes:
        :line: Dockerfile current line.
    '''

    if '-Ur requirements.txt' not in line:
        printError('"-Ur requirements.txt" not found.')
        return True


def getLabelOptions(line):
    ''' This method sets the "labelOptions" dictionary values and return it.

    Attributes:
        :line: Dockerfile current line.
    '''

    for option in labelOptions:
        if option in line:
            labelOptions[option] = True

    return labelOptions


def findInLabelOptions(labelOptions):
    ''' This method checks if there\'s any LABEL statement in Dockerfile
        and if it contains the minimum required options.

    Attributes:
        :labelOptions: Dictionary with LABEL instruction options.
    '''

    if len(labelOptions) == 0:
        printError('Instruction LABEL not found in Dockerfile.')
        return True

    for option in labelOptions:
        if not labelOptions[option]:
            printError('Option "{}" missing in LABEL instruction.'.format(option))
            return True


def printAlreadyRemoveInBlock(nLine):
    ''' This method prints an error when the "rm" program is executed more
        than once in the block of the same instruction.

    Attributes:
        :nLine: Line number where the "rm" program has been found.
    '''

    printError('Command "rm" already used in line {}.'.format(nLine))
    return True
