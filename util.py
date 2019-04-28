#!/usr/bin/env python3


def isSplittedLine(line):
    return line[0] == ' '


def getInstruction(file, n_line):
    with open(file) as f:
        return f.read().split('\n')[n_line - 1].split(' ')[0]
