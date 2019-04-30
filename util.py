#!/usr/bin/env python3

instCopyList = []


def isSplittedLine(line):
        return line[0] == ' '


def getInstruction(file, n_line):
        with open(file) as f:
                return f.read().split('\n')[n_line - 1].split(' ')[0]


def checkAlreadyCopyDestinations(line):
        destination = line.split(' ')[-1]
        if destination in instCopyList:
                return True
        else:
                instCopyList.append(destination)
                return False


def checkRunAptGetInstall(line):
        if ' -y --no-install-recommends' not in line:
                return True
        else:
                return False
